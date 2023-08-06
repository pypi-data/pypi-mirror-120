#!/usr/bin/env python3
"""A stress test for the DNS infrastructure as well as an example of distributed caching"""

from epicman.objects import callable_entity
from epicman.syscalls import *
from epicman.server import MainLoop

import pytest
import sys

from epicman.middleware.dns import DNSCache, A, AAAA, MX
from dns.rrset import RRset

async def start_app():
    lookups = [
        ('example.org', A),
        ('example.org', AAAA),
        ('example.org', MX),
        ] * 10
    for hostname, typ in lookups:
        reply = await DNSCache[(hostname, typ)].resolve()
        assert isinstance(reply, RRset), 'Unexpected reply recived'
        assert len(reply) > 0, 'Empty reply returned'

    sys.exit(0)

    
def test_dns_tasks():
    main_loop = MainLoop({})

    with pytest.raises(SystemExit):
        main_loop.run_forever([start_app])
