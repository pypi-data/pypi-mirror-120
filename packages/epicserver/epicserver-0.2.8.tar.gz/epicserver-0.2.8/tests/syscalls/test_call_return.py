#!/usr/bin/env python3
from epicman.server import MainLoop, SchedulerError
from epicman.objects import EntityProxy, Entity, remote_call

import pytest
import sys

@EntityProxy
class Return(Entity):
    @remote_call
    async def callee(self, i):
        return i + 1
        
    @remote_call
    async def caller(self, inital=1):
        val = await Return[self.instance].callee(inital)
        assert val is not None, 'Remote val did not return a value, request chaining may be broken'
        assert val == inital + 1, 'remote method did not increment value'
        sys.exit()

async def start():
    app = Return['test']
    await app.caller(4)

def test_chained_call():
    main_loop = MainLoop({}) 

    with pytest.raises(SystemExit):
        main_loop.run_forever([start])
