#!/usr/bin/env python3

from ..logging import log, Level as LogLevel
from ..middleware.mesh import start_app
from ..syscalls import THREAD_SLEEP
from ..version import version

from .utils import port_or_addr, comma_seperated, single_address
from .utils import get_entrypoint

from . import MainLoop, RoutingTable, SchedulerError, LICENSING_URL

from socket import has_dualstack_ipv6, has_ipv6
from argparse import ArgumentParser, FileType, OPTIONAL
from functools import wraps
from time import time as now


POLL_PERIOD = 0.05 # 50ms
ERR_FAILED_CLUSTER_CONNECT = 12

def delay_until_connected(func, routing_table):
    @wraps(delay_until_connected)
    async def inner():
        """We want to ensure we dont try and spawn threads before we are conencted 
        to other cluster members as we do not execute anything locally"""
        DELTA_LOG_INTERVAL = 1 # seconds
        RETRY_MAX_TIME = now() + 5 # seconds
        prev_time = 0
        cur_time = DELTA_LOG_INTERVAL
        while len(routing_table) == 0:
            if cur_time - prev_time >= DELTA_LOG_INTERVAL:
                log.info("Not connected to cluster, waiting to connect")
                prev_time = cur_time
            await THREAD_SLEEP(POLL_PERIOD)
            cur_time = now()
            if cur_time > RETRY_MAX_TIME:
                log.exception("Did not sucsessfully connect to the cluster, exiting", ERR_FAILED_CLUSTER_CONNECT)
                
        log.info("Launching cluster startup code")
        # TODO: remove import
        from ..objects import callable_entity
        startup = callable_entity(func)['startup']
        startup._only_local = True
        # Wait, what if the module does not exist on the other end?
        await startup()
        
        log.info("Cluster started, exiting")
        sys.exit()
    return inner
    

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
    cluster_group.add_argument('-n', '--name', default='epicman',
        help="Name of the cluster, used to allow multiple clusters to coexist (Default: %(default)s)")
    cluster_group.add_argument('-m', '--mdns', action="store_true", default=False,
        help="Use mdns for node discovery")
    cluster_group.add_argument('bootstrap', metavar="ADDR[,ADDR[,...]]",
        type=comma_seperated(single_address), default=[],
        help="Addresses to connect to to join the mesh (Comma seperated address:port pairs)")


    args.add_argument('entrypoint',
        help="Specifies a callable to start the system up in the form module.sub:callable")
    
    options = args.parse_args()
    log.debug("Parsed args")

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

    try:
        startup = get_entrypoint(options.entrypoint)
    except ModuleNotFoundError as err:
        args.error(err)
    except ValueError as err:
        args.error(err)
        

    neighbors = RoutingTable()

    startup = delay_until_connected(startup, neighbors)
    # TODO: replace this with our own connect logic so we dont need a routing table
    cluster_connect = start_app(neighbors, [], options.bootstrap, options.mdns)

    main_loop = MainLoop({}, neighbors)
    try:
        from ..objects import callable_entity
        startup = callable_entity(startup)
        startup._only_local = True
        startup = startup['startup']
        # TODO: this should likley be a new type of callable_entity
        main_loop.call(startup, startup.__call__, (), {})
        main_loop.run_forever([cluster_connect])
#        main_loop.run_forever([startup, cluster_connect])
    except SchedulerError:
        log.info("All running threads have exited, shutting down")
    except KeyboardInterrupt:
        log.info("System requested exit, got SIGINT")


if __name__ == "__main__":
    main()

