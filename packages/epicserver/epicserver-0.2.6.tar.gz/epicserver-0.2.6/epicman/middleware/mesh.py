#!/usr/bin/env python

from ..objects import Entity, EntityProxy, Future, Lock, Queue, remote_call, remote_spawn
from ..helpers.socket import async_socket, get_tcp_info
from ..helpers.utils import retry
from ..logging import log
from ..syscalls import THREAD_SLEEP

from .protocol import Packetize

from ipaddress import IPv6Address

from contextlib import suppress
from typing import Union, List, Tuple
import resource
import socket
import bisect
import json
import pickle

from ..constants import hash_algo


PICKLE_PROTOCOL = 5

PAGE_SIZE = resource.getpagesize()

SPEED_1_MEGABIT = 1_000_000
SPEED_10_MEGABIT = SPEED_1_MEGABIT * 10
SPEED_40_MEGABIT = SPEED_1_MEGABIT * 40
SPEED_100_MEGABIT = SPEED_10_MEGABIT * 10
SPEED_GIGABIT = SPEED_100_MEGABIT * 10
SPEED_10_GIGABIT = SPEED_GIGABIT * 10

HEARTBEAT_PERIOD = 2

@EntityProxy
class S2S(Entity):
    _only_local = True

    def _activate(self):
        self.in_flight_invocations = {}
        self.send_queue = Queue()

    @remote_spawn
    async def ingress_connection(self, conn, routing_table, listen_addrs):
        conn.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, True)
#        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BUSY_POLL, 100) #uS

        # TODO: move to init/activate to avoid double activation
        self.packet = Packetize(conn)
        self.conn = conn

        await self._send_packet() # background worker
        await self.send_updates(routing_table, listen_addrs)
        await self.recv_updates(routing_table)

    @remote_spawn
    @retry(3, 2, (ConnectionError,), suppress=True)
    async def egress_connection(self, routing_table, listen_addrs):
        conn = async_socket(socket.AF_INET6, socket.SOCK_STREAM)
        conn.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, False)
        conn.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, True)
#        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BUSY_POLL, 100) #uS

        self.packet = Packetize(conn)
        self.conn = conn

        addr, port, *_ = self.instance
        addr = str(addr) # this is a ipaddress object

        log.info("Connecting")
        await conn.connect((addr, port))
        log.info("Connected")

        await self._send_packet() # background worker
        await self.send_updates(routing_table, listen_addrs)
        await self.recv_updates(routing_table)


    @remote_call
    async def send_remote_invoke(self, ret_addr, entity_addr: Entity, method, args, kwargs, timeout=0):
        """This is a proxy method to ensure we have a context with a refrence 
        to the original connection so we can send the value back

        this is invoked for call and spawn as spawn should not return on the 
        original host until a None is returned to indicate it has started. 
        this is implicit by @remote_spawn on the called function
        """
        mailbox = Future()
        try:
            self.in_flight_invocations[ret_addr] = mailbox

            # this is an 'EDGE' so we translate the method name to somthing that
            # can be over the wire as a closure will hide the implementation and
            # cause pickle lookups to fail when it checks it can be direct ref'd
            # via __import__()
            msg = ('I', (ret_addr, entity_addr, method.__name__, args, kwargs))
            packet = pickle.dumps(msg, protocol=PICKLE_PROTOCOL)

            await self.send_packet(packet, timeout, future=mailbox)

            value, exception = await mailbox.wait()
        finally:
            del self.in_flight_invocations[ret_addr]

        if exception:
            raise exception
        return value

################################################################################
# TODO: replace these 2 with a singleton as the interaction between the two
#       is effectivly the same thing
    async def send_packet(self, val, timeout=0, future=None):
        notify = future or Future()
        await self.send_queue.append((notify, val))
        ret = await notify.wait(timeout=timeout)
        # TODO: implement and test the following:
        # if ret == 0:
        #   raise ConnectionError()
        return ret

    @remote_spawn
    async def _send_packet(self):
        try:
            while True:
                notify, item = await self.send_queue.pop(0)
                count = await self.packet.send(item)
                await notify.set_value(count)
        except ConnectionError:
            log.info("Remote closed connection")
            self._deactivate()
        except TimeoutError:
            log.info("Remote did not respond in a timely manner, closing")
            self._deactivate()
        finally:
            # connection error, broadcast it out
            for notify, item in self.send_queue:
                await notify.set_value(0)
################################################################################

    # this is a remote_call even in the spawn case as it invokes the dst method
    # and it is that method that wil return imeditatly (spawn) or block (call)
    # without us having to introspect the details but having the behavior 
    # we want
    @remote_call
    async def send_remote_reply(self, ret_addr, entity_addr: Entity, method_name, args, kwargs):
        # Setup
        ret_value = None
        exception = None

        try:
            # this may return an Attribute error which we just pass back
            # via the normal exception handlign mechanism, sould indicate a
            # code mismatch as users should be using helpers always
            method = getattr(entity_addr, method_name)
            
            ret_value = await method(*args, **kwargs)
        except Exception as err:
            exception = err

        # Return the value
        msg = ('i', (ret_addr, ret_value, exception))
        packet = pickle.dumps(msg, protocol=PICKLE_PROTOCOL)

        size = await self.send_packet(packet)


    @remote_spawn
    async def recv_updates(self, routing_table):
        # TODO: Version Check
        annouced_addrs = []
        try:
            async for packet in self.packet.recv(HEARTBEAT_PERIOD):
                op, msg = pickle.loads(packet)
                # Captitals indicate incomming work requests 
                # Lower case for replies/responses/away work
                if op == 'I':
                    log.info("Request for remote spawn of {}", msg[1])
                    # TODO: confirm we are responsible for this addr
                    await self.send_remote_reply(*msg)

                elif op == 'i': # Call reply
                    ret_addr, val, exception = msg
                    log.info("Received reply for thread [{}]", ret_addr)

                    mailbox = self.in_flight_invocations[ret_addr]
                    await mailbox.set_value((val, exception))

                elif op == 'P':
                    log.debug('Recived ping from remote end')

                elif op == '+':
                    hash_addr, addrs = msg
                    addrs = [S2S[addr] for addr in addrs]
                    # TODO: remove hard coded 'first addr' entry
                    FIRST = 0
                    routing_table[hash_addr] = addrs[FIRST]
                    annouced_addrs.append(hash_addr)
                    log.info("Added node to routing table {}: {}", hash_addr.hex().zfill(64), addrs[FIRST])

                elif op == '-':
                    hash_addr, addrs = msg
                    addrs = [S2S[addr] for addr in addrs]
                    # TODO: remove hard coded 'first addr' entry
                    FIRST = 0
                    del routing_table[hash_addr]
                    log.info("Removed node from routing table {}: {}", hash_addr.hex().zfill(64), addrs)

                elif op == 'M':
                    log.debug('Recived migrate to us request from remote end')

                elif op == 'm':
                    log.debug('Recived migrate away from us request from remote end')

                else:
                    raise TypeError(f'Unknown operation {op}', op)

        except ConnectionError:
            log.info("Remote closed connection")
            self._deactivate()
        except TimeoutError:
            log.info("Remote did not respond in a timely manner, closing")
            self._deactivate()
        except pickle.UnpicklingError:
            log.info("Invalid Packet from remote end, closing connection")
            log.info("Closing connection due to previous error")
            self._deactivate()
        finally:
            # BUG: confirm we are deleting the correct entry
            for hash_addr in annouced_addrs:
                log.info("Removed node from routing table: {}", hash_addr.hex().zfill(64))
                del routing_table[hash_addr]
            
    @remote_spawn
    async def send_updates(self, routing_table, listen_addrs=[]):
        try:
            # Send all hashes we are responsible for
            for hash_addr, remote in routing_table:
                if remote is None:
                    msg = ('+', (hash_addr, listen_addrs))
                    packet = pickle.dumps(msg, protocol=PICKLE_PROTOCOL)
                    size = await self.send_packet(packet)

            # connection keep alive with pings
            while True:
                msg = ('P', ())
                packet = pickle.dumps(msg, protocol=PICKLE_PROTOCOL)
                size = await self.send_packet(packet)
                await THREAD_SLEEP(HEARTBEAT_PERIOD/2)
        except ConnectionError:
            log.info("Remote closed connection")
        except TimeoutError:
            log.info("Remote did not respond in a timely manner, closing")
            self._deactivate()
        except TypeError:
            log.error("Attempted to send a value that could not be converted to JSON")
            log.error("message: {msg!r}", msg=msg)
            log.info("Closing connection due to previous error")
            self._deactivate()

    @remote_spawn
    async def listen(self, routing_table):
        log.info(f"Listening for incomming connections on {self.instance}")
        sock = async_socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.conn = sock
        
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, False)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        sock.setsockopt(socket.SOL_TCP, socket.TCP_DEFER_ACCEPT, True)

        addr, port = self.instance
        addr = str(addr) # this is a ipaddress object

        sock.bind((addr, port))
        sock.listen()
        while True:
            conn, addr = await sock.accept()
            await S2S[addr].ingress_connection(conn, routing_table, listen_addrs=[self.instance])


#    async def egress(self, neighbors, addr):
#        # Inital population of entries to go out
#        # TODO: move this compatcted table to the RoutingTable object and just serve that
#        entry_size = hash_algo.digest_size
#        buffer = bytes(len(neighbors) * entry_size)
#        # filter entries to only relavant/non-expired
#        for i, neighbor in enumerate(neighbors):
#            addr, _ = neighbor
#            log.warn(f'xxxxxxxx {addr}')
#            offset = entry_size * i
#            # the bytes() digest may be less than entry_size and need to be prepended
#            # with nulls, rather than create an itnermedite buffer jsut write from
#            # end to start instead
#            buffer[offset + entry_size:offset:-1] = addr[::-1]
#
#        from math import ceil
#        packet_count = len(buffer) / mtu
#        # round up to ensure trailing entries are sent
#        packet_count = ceil(packet_count)
#        for i in range(packet_count):
#            offset = mtu * i
#            await self.conn.send(buffer[offset:offset+mtu])
#
#        if latency < 20ms:
#            sock.setsockopt(socket.TCP_CONGESTION, 'datacenter')
#        else:
#            sock.setsockopt(socket.TCP_CONGESTION, 'codel')
#        # get path MTU
#        IPV6_PMTU = 23
#        PMTU_DONT  = 0
#        PMTU_WANT  = 1
#        PMTU_DO    = 2
#        PMTU_PROBE = 3
#        IPV6_MTU = 24
#        IPV6_HEADER_LEN = 40
#        ETHER_HEADER = 22
#        # get inital MTU estimate
#        mtu = conn.getsockopt(socket.IPPROTO_IPV6, IPV6_MTU)
#        mtu -= IPV6_HEADER_LEN
#        mtu -= ETHER_HEADER_LEN
#        # let network fragment
#        conn.setsockopt(socket.IPPROTO_IPV6, IPV6_PMTU, PMTU_PROBE)
#        conn.send(LARGE_PACKET)
#        # network should have updaetd us via icmpv6, shring MTU and get updates
#        mtu = conn.getsockopt(socket.IPPROTO_IPV6, IPV6_MTU)
#        mtu -= IPV6_HEADER_LEN
#        mtu -= ETHER_HEADER_LEN
#        conn.setsockopt(socket.IPPROTO_IPV6, IPV6_PMTU, PMTU_DO)
#
#        data, err_queue, flags, addr = con.recvmsg(size, err_size, socket.MSG_ERRQUEUE)
#        if socket.MSG_ERRQUEUE & flags:
#            # do we have an MTU update?
#            for lvl, typ, data in err_queue:
#                if lvl == IPPROTO_IPV6 and type == IPV6_MTU?
        
#        while data:
#            try:
#            #    data, ancdata, flags, addr = conn.recvmsg(MTU)
#                count = conn.send(data[:mtu])
#                data = data[count:]
#            except OSError:
#                # OSError: [Errno 90] Message too long
#                mtu = blah

    def _deactivate(self):
        # AttributeError: raised if no 'conn' object on self
        # ValueError: Raised if the fd is closed (fd=-1)
        with suppress(AttributeError, ValueError):
            self.conn.close()

def start_app(neighbors: 'Routing', listen: List[Tuple[IPv6Address, int]], hints: List[Tuple[str, int]] = [], mdns=False):
    async def start_app():
        for addr in listen:
            await S2S[addr].listen(neighbors)
#            await S2S[addr].ingress(neighbors)
        for hint in hints:
#            await S2S[hint].connect(neighbors)
            # TODO: does not handle multiple listen addr's currently
#            await S2S[hint].egress_connection(neighbors, listen[0][0], listen[0][1])
            await S2S[hint].egress_connection(neighbors, listen)
        if mdns:
            log.info('we should launch a mdns listener here')
    return start_app

    async def start_app():
        s = async_socket(socket.AF_INET6, socket.SOCK_STREAM)
        s.setblocking(False)
        # These options are tunned for LAN/Datacenter level latencies
        # taking more than one second for rtt is highly unlikley
        # with 1-2mS expected
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        s.setsockopt(socket.SOL_TCP,    socket.TCP_NODELAY, True)
        ###### NON PORTABLE OPTIONS ######
#        s.setsockopt(socket.SOL_SOCKET, socket.SO_BUSY_POLL, 100)  # uS
        s.setsockopt(socket.SOL_TCP,    socket.TCP_DEFER_ACCEPT, 3)
        # connection level service monitoring
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        s.setsockopt(socket.SOL_TCP,    socket.TCP_KEEPIDLE, 1)
        s.setsockopt(socket.SOL_TCP,    socket.TCP_KEEPINTVL, 1)
        # We use 500mS here as it allows for some congestion on the remote end
        # though it does not include processing time as this is ourside of
        # the scope of this TCP level monitor
        s.setsockopt(socket.SOL_TCP,    socket.TCP_USER_TIMEOUT, 500)  # mS
#        s.setsockopt(socket.SOL_IP,     socket.IP_RECVERR, True) #mS
        addr = ('127.0.0.1', 30303)
        s.bind(addr)
        s.listen()


def calc_buffer_size(sock: socket.socket, link_speed: int = SPEED_GIGABIT):
    # tcpi_rcv_rtt - how long in uS that the remote client would exaust the current window
    tcp_info = get_tcp_info(sock)
    round_trip_time = tcp_info.tcpi_rtt
    buffer_size = link_speed * round_trip_time

    # Convert to bytese
    buffer_size /= 8
    # truncate lower bit to be a multiple of PAGE_SIZE
    buffer_size /= PAGE_SIZE
    # Add one additional PAGE_SIZE for saftey
    buffer_size += 1
    buffer_size *= PAGE_SIZE

    return buffer_size


class Routing():
    monitored: list  # Monitored nodes we are always conencted to
    connected: list  # Nodes we have connected to but are not part of montioring policy
    known: list  # all known nodes picked up from gossip

    def __init__(self):
        self.table = RoutingTable

    async def connect(self, entity_addr):
        node = self.ring[entity_addr]
        if node in self.monitored:
            return self.monitored[node]
        elif node in self.connected:
            return self.connected[node]
        else:
            sock = async_socket(socket.AF_INET6, socket.SOCK_STREAM)
            await sock.connect(node.addr)
            return sock

    async def recv_msg(self, socket):
        pass

    async def send_msg(self, task, msg):
        pass


class RoutingTable():
    def __init__(self):
        self.keys = []
        self.values = {}
        
    def __iter__(self):
        yield from list(self.values.items())

    def __getitem__(self, key):
        if len(self) == 0:
            raise KeyError("Routing table is empty")

        i = bisect.bisect_left(self.keys, key)
        if i == len(self):
            addr = self.keys[-1]
        else:
            addr = self.keys[i]
            upper = self.keys[i-1]
            if key < addr:
                addr = upper

        return self.values[addr]            

    def __setitem__(self, key, val):
        bisect.insort_left(self.keys, key)
        # BUG: multi values
        self.values[key] = val

    def __delitem__(self, key):
        try:
            i = bisect.bisect_left(self.keys, key)
            if self.keys[i] != key:
                raise KeyError(key)
            # BUG: are we deleting the same key we look up?
            del self.keys[i]
        except IndexError:
            raise KeyError(key)

    def __repr__(self):
        return f'<RoutingTable items={len(self.keys)}>'

    def __contains__(self, key):
        i = bisect.bisect_left(self.keys, key)
        return self.keys[i] == key

    def __len__(self):
        return len(self.keys)
