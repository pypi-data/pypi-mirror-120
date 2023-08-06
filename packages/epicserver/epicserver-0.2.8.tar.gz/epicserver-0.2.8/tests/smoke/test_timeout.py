#!/usr/bin/env python3

from epicman.objects import callable_entity
from epicman.syscalls import *
from epicman.server import MainLoop

from time import time as now

import pytest
import math
import sys

TASK_START = object()
TIMEOUT = 0.2

async def delayed_termination():
    try:
        await sleeper['test'](timeout=TIMEOUT)
    except TimeoutError as err:
        sys.exit(0)
    pytest.fail("Did not recive a TimeoutError")


@callable_entity
async def sleeper():
    await THREAD_SLEEP(timeout=TIMEOUT*5)


def test_timeout():
    main_loop = MainLoop({})

    start = now()
    with pytest.raises(SystemExit):
        main_loop.run_forever([delayed_termination])
    end = now()

    period = end - start

    assert period >= TIMEOUT, "Slept time was shorter than specified timeout"
    assert math.isclose(period, TIMEOUT, rel_tol=0.05), "Timeout was not within 5% of target time"

