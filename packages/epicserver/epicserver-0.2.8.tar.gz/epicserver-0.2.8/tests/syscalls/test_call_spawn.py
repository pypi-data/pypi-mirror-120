#!/usr/bin/env python3
from epicman.server import MainLoop, SchedulerError
from epicman.objects import EntityProxy, Entity, remote_spawn
from epicman.syscalls import THREAD_SLEEP

from random import randint
import pytest
import sys

# This test uses sleep to enforce schduling order
# and is confirming that both threads are executing concurrently
# (not in parallel). specifically communication must happen out
# of band and not via return value like remote_call

# Caller                        | Callee
# ----------------------------------------------
# Spawn Callee                  |
# Check return val is None      |
# Sleep 1s                      |
#                               | Increment test value
#                               | Sleep 1s
# Check test value increased    |
# exit                          |
#                               | exit

@EntityProxy
class Spawn(Entity):
    number = 0
    @remote_spawn
    async def callee(self):
        self.number += 1
        await THREAD_SLEEP(timeout=1)
        
    @remote_spawn
    async def caller(self, inital):
        self.number = inital
        
        val = await Spawn[self.instance].callee()
        assert val is None, 'spawned threads do not return a value'
        await THREAD_SLEEP(timeout=1)
        
        assert self.number == inital + 1, 'remote method did not increment value'

        sys.exit()

async def start():
    app = Spawn['test']
    await app.caller(randint(0, 100))

def test_chained_call():
    main_loop = MainLoop({}) 

    with pytest.raises(SystemExit):
        main_loop.run_forever([start])
