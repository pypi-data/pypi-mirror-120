#!/usr/bin/env python3

from epicman.logging import _log, Level
from epicman import running_thread, DEFAULT_THREAD
from io import StringIO

import pytest

MSG = 'my message'

@pytest.fixture
def logger():
    context = running_thread.set(DEFAULT_THREAD)
    log = _log(StringIO(), Level.DEBUG)
    try:
        yield log
    finally:
        running_thread.reset(context)

@pytest.mark.parametrize('level',
    ['debug',
     'info',
     'warn',
     'error',
    ])
def test_level(logger, level):
    log = getattr(logger, level)
    log(MSG)
    
    logger.stream.seek(0)
    logged = logger.stream.read()

    # NEWLINE added as this is somthing print() does
    # Logging module uses contextvar to determing currently running
    # we strip the first 18 chars as this holds a timestamp
    assert logged[18:] == f'{DEFAULT_THREAD} {MSG}\n'
    # 1625447697.3766823
    assert logged[:10].isdigit()
    assert logged[10] == '.'
    assert logged[11:17].isdigit()
