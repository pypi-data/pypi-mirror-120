#!/usr/bin/env python3

from functools import wraps
from ..logging import log
from ..syscalls import THREAD_SLEEP

def retry(attempts, delay, exceptions=(Exception,), *, suppress=False):
    def wrapper(func):
        @wraps(func)
        async def _retry(*args, **kwargs):
            for i in range(attempts - 1):
                # we add one to start at '1'
                attempt = i+1
                try:
                    return await func(*args, **kwargs)
                except exceptions as err:
                    log.error("Thread crashed with {err!r}", err=err)
                    # we add 1 to attempts again as we are refering to the 
                    # next attempt we are making
                    log.info("Retrying in {delay}s (Attempt {i}/{attempts})", delay=delay, i=attempt+1, attempts=attempts)
                    await THREAD_SLEEP(delay)
            try:
                return await func(*args, **kwargs)
            except exceptions as err:
                log.error("Thread crashed with {err!r}", err=err)
                if not suppress:
                    raise
        return _retry
    return wrapper
