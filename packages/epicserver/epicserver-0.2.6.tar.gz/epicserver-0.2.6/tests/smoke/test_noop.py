#!/usr/bin/env python3

from epicman.objects import callable_entity
from epicman.syscalls import *
from epicman.server import MainLoop

from time import time as now
import pytest
import sys

DELAY = 0.2

async def start_app():
    await delayed_termination['wait']()

@callable_entity
async def delayed_termination():
    await THREAD_SLEEP(DELAY)
    sys.exit(0)

def test_minimal_tasks():
    main_loop = MainLoop({})

    start = now()
    with pytest.raises(SystemExit):
        main_loop.run_forever([start_app])
    end = now()
    assert end-start >= DELAY, 'Sleep did not delay by correct ammount'
