#!/usr/bin/env python3
# This is used in help output
"""EpicMan Server is used to run an application across multiple process across 
a network. It can run in either standalone mode or in clustered mode. See the 
section [Clustering Settings] for more information on running the networked 
version."""

from ..logging import log, Level as LogLevel
from ..objects import Entity, callable_entity
from .. import running_thread, DEFAULT_THREAD
from ..syscalls import *  # noqa: F403
from ..syscalls import SYSCALL
from ..version import version

# Middleware
from ..middleware.mesh import RoutingTable, start_app, hash_algo as routing_hash_algo

from .utils import get_entrypoint, set_process_affinity
from .utils import port_or_addr, comma_seperated, single_address
from .db import get_backend

from selectors import DefaultSelector as Selector, EVENT_READ, EVENT_WRITE
from dataclasses import dataclass
from collections import defaultdict
from typing import Optional, Union, Dict, List, Tuple, Set, Any, Generator, Callable
from argparse import ArgumentParser, OPTIONAL
from contextlib import suppress
from socket import gethostbyname_ex, getfqdn, has_dualstack_ipv6, has_ipv6
from time import time
from errno import EISCONN

from itertools import count

import traceback
import pickle
import signal
import sys


def debug_handler(*args):
    breakpoint() # noqa

# we use a possitive time here rather than None to pass to our selector as we
# need to do mathemtical comparision between several timeout numbers (see
# min() and next_* below). 1s was chosent o ensure we are waking up on a
# regular basis without causing too much IO overhead. This should allow us to
# put regular house keeping tasks in (eg GC)
BLOCK = 1
NO_WAIT = -1

# For use with delayed_time as entry and filed acessor names
FIRST = 0
DELAY_TIME = 0

# Used as sentinal in RoutingTable/neighbors
SELF = None

# exit codes
ERR_NO_IPV6 = 10

LICENSING_URL = "http://www.epic-man.com/license?src=ipv6only"

class EpicError(Exception):
    pass

class SerializationError(EpicError):
    pass

class SchedulerError(EpicError):
    pass

class EntityPersistError(EpicError):
    def __str__(self):
        return f"Error encountered while persisting entity: {self.arg[0]}"


def _sock_recv(syscall):
    return EVENT_READ, syscall.file.recv, (syscall.size, syscall.flags)

def _sock_recvfrom(syscall):
    return EVENT_READ, syscall.file.recvfrom, (syscall.size, syscall.flags)

def _sock_accept(syscall):
    return EVENT_READ, syscall.file.accept, ()

def _sock_connect1(syscall):
    def callback(file, addr):
        try:
            file.connect(addr)
        except BlockingIOError:
            pass
        return True
    return EVENT_WRITE, callback, (syscall.file, syscall.addr,)

def _sock_connect2(syscall):
    def callback(file, addr):
        try:
            file.connect(addr)
        except OSError as err:
            if err.errno == EISCONN:
                return True
            raise
    return EVENT_WRITE, callback, (syscall.file, syscall.addr)

def _sock_send(syscall):
    return EVENT_WRITE, syscall.file.send, (syscall.data, syscall.flags)

def _sock_sendmsg(syscall):
    return EVENT_WRITE, syscall.file.sendmsg, (syscall.buffers, syscall.ancdata, syscall.flags, syscall.address)

def _sock_sendto(syscall):
    return EVENT_WRITE, syscall.file.sendto, (syscall.data, syscall.flags, syscall.address)

def _file_read(syscall):
    return EVENT_READ, syscall.file.read, (syscall.size,)

def _file_write(syscall):
    return EVENT_WRITE, syscall.file.write, (syscall.data,)

SYSCALL_HANDLERS = {
    SOCK_RECV:     _sock_recv,
    SOCK_RECVFROM: _sock_recvfrom,
    SOCK_ACCEPT:   _sock_accept,
    SOCK_CONNECT1: _sock_connect1,
    SOCK_CONNECT2: _sock_connect2,
    SOCK_SEND:     _sock_send,
    SOCK_SENDMSG:  _sock_sendmsg,
    SOCK_SENDTO:   _sock_sendto,
    FILE_READ:     _file_read,
    FILE_WRITE:    _file_write,
    }

@dataclass
class Thread:
    addr: Tuple[Entity, Any]
    id: int
    state: Generator[SYSCALL, Any, Any]

    syscall_result = None
    syscall_error = None
    current_syscall = None

    caller: "Thread" = None

    def __str__(self):
        return f'[{self.addr}][{self.state.__name__}][{self.id}]'

class MainLoop():
    cancelable_syscall: List[Tuple[Union[float, int], Thread]]

    storage = None
    neighbors = None
    selector = None

    entities: Dict[Tuple[Entity, Any], Entity]
    runnable_threads: List[Thread]
    threads: List[Thread]
    _next_thread_id: Callable

    def __init__(self, storage, neighbors=None):
        # operating in non clustered mode, all 'location' requests should
        # just return ourselves
        if neighbors is None:
            neighbors = RoutingTable()
            neighbors[b'0'] = SELF
        self.neighbors = neighbors
        self.storage = storage
        self.selector = Selector()

        self.entities = {}
        self.runnable_threads = []
        self.cancelable_syscall = []
        self.waiters = defaultdict(list)
        self.threads = []
        # thread id = 0 is reserved for the system so we use the next freely avlible one
        self._next_thread_id = count(1)

    # reentiriancy implemented with locks on entity state and decorator
    def call(self, addr, method, args, kwargs) -> Thread:
        """raises attribute error is method does not exist"""
        if addr not in self.entities:
            saved_state = self.storage.get(addr, {})
            entity_instance = addr._restore(addr.instance, saved_state)
            # is we had no persisted state then allow the entity
            # to initalise its starting state
            if not saved_state:
                entity_instance._activate()
            self.entities[addr] = (entity_instance, [])
        # This ensures we can share state between threads
        entity_instance, threads = self.entities[addr]

        method = getattr(entity_instance, method.__name__)
        implementation = method._implementation
        # we provide the 'self' arg here as the entity instance
        # as we detach the implementation from a class and not
        # an instance of the class and therefore it has no idea
        # what it shoudl be bound to
        state = implementation(entity_instance, *args, **kwargs)

        thread_id = next(self._next_thread_id)

        thread = Thread(addr, thread_id, state)

        # Allow Entities to track what threads are running across
        # thier state to allow us to GC them when unused
        threads.append(thread)
        log.info('New Thread created: [{}]', thread.id)

        self.schedule(thread)

        return thread

    def schedule(self, thread: Thread):
        self.runnable_threads.append(thread)
        self.threads.append(thread)
        # we have the result, cancel all pending io and timeouts
        # so these dont come along and invalidate out result
        self.unregister_io(thread)

    def unschedule(self, thread: Thread):
        entity, threads = self.entities[thread.addr]
        threads.remove(thread)
        if not threads:
            self.persist(thread.addr)
            log.info('Entity has been persisted')

            del self.entities[thread.addr]
            entity._deactivate() # give entity a chance to clean itself up
            log.info('Entity has no remaining threads, terminating')
        try:
            self.runnable_threads.remove(thread)
        except ValueError:
            pass
        self.threads.remove(thread)
        self.unregister_io(thread)

    def persist(self, addr, state=None):
        if not isinstance(state, dict):
            entity, _ = self.entities[addr]
            state = entity._save()
            if state is None:
                # sentinal value to say 'do not save me'
                return

        self.storage[addr] = state

    def run_io(self):
        # only perform blocking IO if we have IO to be waited on
        # or if we have to pause to a task as we use select()
        # instead of time.sleep()
        if self.selector.get_map() or self.cancelable_syscall:
            next_tick = NO_WAIT
            if not self.runnable_threads:
                next_tick = BLOCK

            next_cancel = BLOCK
            if self.cancelable_syscall:
                # we defer sorting until we need it so we can
                # accumulate changes and only sort once
                self.cancelable_syscall.sort()
                next_cancel = self.cancelable_syscall[FIRST][DELAY_TIME] - time()

            next_tick = min(next_tick, next_cancel)

            for event, event_type in self.selector.select(next_tick):
                thread, call, args = event.data
                try:
                    ret = call(*args)
                except BlockingIOError:
                    # this case is mainly hit for accept() and
                    # multithreaded/process code listening on the
                    # same port as on a conneciton multiple
                    # tasks/threads may be awoken
                    # we want to reschedule in that case
                    continue
                except Exception as err:
                    # reinject all other errors to handling task
                    # should allow compatibility with exitsting
                    # socket code until we can enumerate all the
                    # cases
                    thread.syscall_error = err
                    self.schedule(thread)
                else:
                    # no issues occured so we can reschedule the process
                    thread.syscall_result = ret
                    self.schedule(thread)

    # TODO: this should really be timeout not timedout
    def run_timedout(self):
        now = time()
        while self.cancelable_syscall:
            wake_time, thread = self.cancelable_syscall[FIRST]
            if wake_time > now:
                break
            self.unregister_io(thread)
            thread.syscall_error = TimeoutError("Syscall Timer expired", thread.current_syscall)
            thread.syscall_value = None
            self.schedule(thread)

    def unregister_io(self, thread):
        with suppress(ValueError):
            for i, cancel in enumerate(self.cancelable_syscall):
                t, c_thread = cancel
                if c_thread == thread:
                    del self.cancelable_syscall[i]
                    break
        file = getattr(thread.current_syscall, 'file', None)
        if file:
            with suppress(KeyError, ValueError):
                self.selector.unregister(file)

    def run_forever(self, inital_threads: List[Callable]):
        for startup_task in inital_threads:
            # we take async functions here not Entities
            entity = callable_entity(startup_task)['startup']
            self.call(entity, entity.__call__, (), {})

        while True:
            self.run_once()
            self.run_io()
            self.run_timedout()

            if not any((self.runnable_threads, self.cancelable_syscall, self.selector.get_map())):
                raise SchedulerError("No runnable threads or IO left")

    def run_once(self):
        syscall: SYSCALL

        try:
            threads = self.runnable_threads
            self.runnable_threads = []
            for thread in threads:
                running_thread.set(thread)
                log.debug("Thread running")
                try:
                    if thread.syscall_error:
                        syscall = thread.state.throw(thread.syscall_error)
                    else:
                        syscall = thread.state.send(thread.syscall_result)

                except AssertionError:
                    # required to use asserts in threads in test framework
                    # This case happens after first await till function exit
                    raise

                except StopIteration as err:
                    log.info('Thread Exited')
                    if thread.caller:
                       thread.caller.syscall_result = err.value
                       self.schedule(thread.caller)
                    self.unschedule(thread)

                    continue

                except Exception as err:
                    # TODO: will this affect the JIT?
                    log.error("=== Current Syscall ===")
                    log.error("{current} = {result}",
                                current=thread.current_syscall,
                                result=(thread.syscall_result or thread.syscall_error))
                    if thread.caller:
                        log.error("=== Caller Stack ===")
                        stack = traceback.format_stack(thread.caller.state.cr_frame)
                        log.error('| ' + '| '.join(stack))
                    log.error("====================")

                    self.unschedule(thread)
                    log.error('Thread Crashed with "{err}"',
                                err=err, 
                                _err=sys.exc_info())

                    continue

                ## Reset state to prevent inadvertant leakage of state from 
                ## prev call
                thread.syscall_result = None
                thread.syscall_error = None
                thread.current_syscall = syscall

                ### Features common to all syscalls
                # TODO: remove conditional as we will use MAX_DELAY to sort
                #       anything 'blocking forever' to end of delay list
                #       see objects.py for the other todo msg
                if syscall.timeout:
                    wake_time = syscall.timeout + time()
                    self.cancelable_syscall.append((wake_time, thread))

                action = SYSCALL_HANDLERS.get(syscall.__class__, None)
                if action:
                    try:
                        event, call, args = action(syscall)
                        self.selector.register(syscall.file, event, (thread, call, args))
                    except ValueError as err:
                        # you cant register a closed (fd=-1) fd, convert this to 
                        # a subclass of ConnectionError to allow existing error
                        # handling to work with minimal modification
                        thread.syscall_error = BrokenPipeError("fd is closed")
                        self.schedule(thread)
                    except PermissionError as err:
                        thread.syscall_error = PermissionError(err.errno, 'Operation not permitted, is this a normal file?')
                        self.schedule(thread)
                    except Exception as err:
                        thread.syscall_error = err
                        self.schedule(thread)

                # THREAD_SLEEP is implemented as a noop timeout/cancelable 
                # syscall this is here to avoid the catch-all at the end
                elif isinstance(syscall, THREAD_SLEEP):  # noqa: F405
                    pass

                elif isinstance(syscall, FUTURE_WAIT):  # noqa: F405
                    self.waiters[syscall.future].append(thread)

                elif isinstance(syscall, FUTURE_NOTIFY):  # noqa: F405
                    # What do we notify?
                    for waiting_thread in self.waiters[syscall.future]:
                        # we may have a timeout ongoing
                        self.unregister_io(waiting_thread)
                        # The future handles returning the correct val
                        # So just reset the syscall_* to avoid issues
                        waiting_thread.syscall_result = None
                        waiting_thread.syscall_error = None
                        self.schedule(waiting_thread)
                    # Kill off the wait queue to avoid a mem leak
                    del self.waiters[syscall.future]
                    # and reschedule the caller as well
                    self.schedule(thread)

                elif isinstance(syscall, (ENTITY_CALL, ENTITY_SPAWN)):  # noqa: F405
                    entity_addr = str(syscall.addr).encode('ascii')
                    entity_addr = routing_hash_algo(entity_addr).digest()

                    try:
                        node = self.neighbors[entity_addr]
                    except KeyError:
                        # we expect to hit this case if we are epicman-server-startup
                        node = None
                    local = syscall.addr._only_local or (node is None)

                    if local:
                        log.info('Creating new local thread: [{}][{}]', syscall.addr, syscall.method.__name__)
                        called_thread = self.call(syscall.addr, syscall.method, syscall.args, syscall.kwargs)
                        if isinstance(syscall, ENTITY_SPAWN):  # noqa: F405
                            # reschedule the caller
                            self.schedule(thread)
                        else:
                            # set up reverse chaining
                            called_thread.caller = thread
                    else:
                        log.info('Creating new remote thread: [{}][{}]', syscall.addr, syscall.method.__name__)
                        try:
                            ret_thread = thread.id
                            called_thread = self.call(node,
                                                      node.send_remote_invoke,
                                                      (ret_thread, syscall.addr,
                                                        syscall.method,
                                                        syscall.args,
                                                        syscall.kwargs),
                                                      {})
                            called_thread.caller = thread
                        except pickle.UnpicklingError as err:
                            log.warn("Unable to send message as parts or addr cannot be serialised")
                            thread.syscall_error = SerializationError(err)
                            thread.syscall_result = None
                            self.schedule(thread)

                elif isinstance(syscall, GET_NAME):  # noqa: F405
                    # TODO: wire this up to async dnspython - turn this into a SEND to dnspython
                    addrs = gethostbyname_ex(syscall.name)[2]
                    thread.syscall_result = addrs
                    self.schedule(thread)

                elif isinstance(syscall, CHECKPOINT):  # noqa: F405
                    thread.syscall_result = False
                    try: # nosec
                        self.persist(thread.addr, syscall.state)
                        thread.syscall_result = True
                    except Exception as err:
                        thread.syscall_error = EntityPersistError(err)
                        log.error('Could not persist Entity due to "{err}"', err=err, _err=sys.exc_info())
                    # reschedule the thread
                    self.schedule(thread)

                else:
                    log.error('Client worker called unrecognised syscall "{syscall}", exiting', syscall=syscall)
                    self.unschedule(thread)
                    try:
                        thread.state.close()
                    except Exception: # nosec
                        # we dont care if it blows up, we cant do anything
                        pass
                    continue
        except Exception as err:
            if thread.caller:
                log.error("=== Caller Stack ===")
                stack = traceback.format_stack(thread.state.cr_frame)
                log.error('| ' + '| '.join(stack))
                log.error("====================")
            raise
        finally:
            running_thread.set(DEFAULT_THREAD)


def main():
    args = ArgumentParser(
        description=__doc__,
        fromfile_prefix_chars="@",
        epilog='Additional arguments can be read from a file by adding '
               'the path to the file as an argument prepended with "@". '
               'This can be used to implement profiles for certain '
               'Applications.'
        )
    args.add_argument('-v', '--verbose', action='count', default=0,
        help="More verbose logging, specify multiple times for more logging")
    args.add_argument('-V', '--version', action='version', version=version,
        help="Print the version and exit")

    cluster_group = args.add_argument_group('Clustering Settings',
        description='The section describes the "clustered mode" that allows '
                    'you to run an Application over multiple nodes. '
                    'When running in clustered mode "-l" must be given to '
                    'allow other Nodes to connect in. For the initial node this '
                    'MAY be the only option that needs specifying, all other '
                    'nodes after this will need at least one discovery option '
                    'enabled.')
    cluster_group.add_argument('-l', '--listen', 
        metavar="ADDR", type=port_or_addr,
        default=[], action='append',
        help="Port to list on for server to server (S2S) connections (Default: Disabled)")
    cluster_group.add_argument('-n', '--name', default='epicman',
        help="Name of the cluster, used to allow multiple clusters to coexist (Default: %(default)s)")
    cluster_group.add_argument('-m', '--mdns', action="store_true", default=False,
        help="Use mdns for node discovery")
    cluster_group.add_argument('-b', '--bootstrap', metavar="ADDR[,ADDR[,...]]",
        type=comma_seperated(single_address), default=[],
        help="Addresses to connect to to join the mesh (Comma seperated address:port pairs)")
    cluster_group.add_argument('-p', '--positions', default=1, type=int,
        help="How many positions on the mesh to occupy, roughly equal to a load factor (Default: %(default)s)")

    args.add_argument('-c', '--cpu', default=None,
        help='Comma sepperated list of cpus to execute on (Default: All avalible CPUS)')
    args.add_argument('-d', '--database', default="default://epicman.db", metavar="URL",
        help='Database connection string to seralize game Entitys (Default: %(default)s):')
    args.add_argument('entrypoint', default="epicman.helpers:dummy_app", nargs=OPTIONAL,
        help="Specifies a callable to start the system up in the form module.sub:callable")
    options = args.parse_args()
    log.info("Parsed args")

    # cap the value to valid ranges
    max_verbosity = max(LogLevel.__members__.values()).value
    options.verbose = min(options.verbose, max_verbosity)
    options.verbose = LogLevel(options.verbose)
    log.log_level = options.verbose
    log.info(f"Log verbosity changed to {options.verbose.name}")

    if not has_ipv6:
        log.info('IPv4 support is a commercial subscription feature, see {LICENSING_URL} for more information on licensing')
        log.exception("No IPv6 support, exiting as this is an IPv6 native application", ERR_NO_IPV6)
        
    if not has_dualstack_ipv6():
        log.warn("IPv6 implementation is not dueal stack (IPv4 via IPv6), you may encounter connection issues to IPv4 hosts")

    if options.cpu:
        try:
            set_process_affinity(options.cpu)
        except ValueError:
            args.error(f'The provided cpu mask is invalid: "{options.cpu}"')

    apps = []

    neighbors = RoutingTable()
    if options.listen:
        # This string has to be a bit special
        #  Options.name: Not strictly required for uniqueness
        #  hostname: THIS MAY BE SET INCORRECTLY BY ADMIN, but we need to include it
        #            to disambiguate the 'addr' below when set to '' and not an IP
        #  Options.listen[addr]: when not the all addresses '' should be globally 
        #                        unique
        #  Options.listen[port]: This is only unique on the context of a machine
        for i in range(options.positions):
            node_id = f'{options.name}-{getfqdn()}-{options.listen[0][0]}-{options.listen[0][1]}-{i}'
            node_id = node_id.encode('utf-8')
            self = routing_hash_algo(node_id).digest()
            log.debug("Occupying position on routing table {}", self.hex())
            neighbors[self] = SELF
        apps.append(start_app(neighbors, options.listen, options.bootstrap, options.mdns))
    elif any((options.mdns, options.bootstrap)):
        args.error("--listen must be specified if -n, -m or -b specified")
    else:
        self = routing_hash_algo(b'self').digest()
        neighbors[self] = SELF

    try:
        db = get_backend(options.database)
    except KeyError as err:
        args.error(f"Invalid database type: {err.args[0]}")
    except ValueError as err:
        args.error(f"Invalid database options: {options.database} - {err}")
    except Exception as err:
        args.error(f"Error while creating database - {err}")

    try:
        server_init = get_entrypoint(options.entrypoint)
    except ModuleNotFoundError as err:
        args.error(err)
    except ValueError as err:
        args.error(err)
    apps.append(server_init)

    if __debug__:
        # breakpoint() never passes in the traceback and hence why we use
        # the lambda to use sys.last_traceback and kill off any args
        import pdb
        sys.excepthook = lambda *args: pdb.pm()
        # Debug handler is diffrent as there is no existing traceback 
        # currently occuring so we can just invoke the debugger as is
        signal.signal(signal.SIGUSR1, debug_handler)

    main_loop = MainLoop(db, neighbors)
    main_loop.run_forever(apps)


if __name__ == "__main__":
    import bdb
    try:
        main()
    except SchedulerError:
        log.info("All running threads have exited, shutting down")
        sys.exit(10)
    except bdb.BdbQuit:
        pass
    except KeyboardInterrupt:
        log.info("System requested exit, got SIGINT")
