#!/usr/bin/env python3


from epicman.objects import EntityProxy, Entity, remote_call, callable_entity
from epicman.syscalls import *
from epicman.server import MainLoop

import pytest
import sys

NUM_OF_PINGS = 1000
NUM_IN_RING = 20

@EntityProxy
class Ping(Entity):
    def _activate(self):
        next_id = (self.instance + 1) % NUM_IN_RING
        self.other = next_id@Ping

    @remote_call
    async def ping(self, i):
        i -= 1
        if i <= 0:
            sys.exit()
        await self.other.ping(i)

async def start_app():
    await Ping[0].ping(NUM_OF_PINGS)

def test_ping_loop():
    main_loop = MainLoop({})

    with pytest.raises(SystemExit):
        main_loop.run_forever([start_app])
