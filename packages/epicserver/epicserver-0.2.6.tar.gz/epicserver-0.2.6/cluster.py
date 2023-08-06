#!/usr/bin/env python3
"""Example test code
"""

from epicman.objects import EntityProxy, Entity, remote_spawn, remote_call
from epicman.syscalls import THREAD_SLEEP
from epicman.logging import log

TOTAL_COUNT = 1000

class _Test(Entity):
    @remote_spawn
    async def test(self, val):
        log.info('Doing some work')
        return val + 1
Test = EntityProxy(_Test)

# local only
async def start():
    count = 0
    for i in range(TOTAL_COUNT):
        count = count or 0
        count = await Test[i].test(count)
#    for i in range(10):
#        await THREAD_SLEEP(0.2)
#        count = await Test[i].test(count)

    log.info('Value: {count}', count=count)
#    assert count == TOTAL_COUNT
    print('done')
    import sys
    sys.exit()
