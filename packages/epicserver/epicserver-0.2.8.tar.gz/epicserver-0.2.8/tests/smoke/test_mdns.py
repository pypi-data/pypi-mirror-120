#!/usr/bin/env python3

from epicman.objects import callable_entity
from epicman.syscalls import THREAD_SLEEP
from epicman.server import MainLoop
from epicman.middleware.dns.mdns import MDNS

import pytest
import sys

test_instance = ('testing', 8080)

async def browse_view():
    # make sure we have a record to return to trigger the exit
    mdns = test_instance@MDNS
    await mdns.publish()

    async for x in mdns.browse():
        breakpoint()
        sys.exit(0)
    assert False, 'did not discover self advertisment'

async def register_mdns():
    mdns = test_instance@MDNS
    await mdns.publish()

async def terminate_if_slow():
    await THREAD_SLEEP(timeout=3)
    assert False, 'Test timed out waiting for mdns to work'

# We need to run a register and brwoser at the same time so we have somthing
# to listen to or else we gat a hang here
@pytest.mark.skip(reason="avahi tools are buggy, especially in mixed IPv4/6 environments")
def test_mdns():
    main_loop = MainLoop({})

    with pytest.raises(SystemExit):
        main_loop.run_forever([browse_view, register_mdns, terminate_if_slow])
