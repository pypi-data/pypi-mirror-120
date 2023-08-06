#!/usr/bin/env python3

from pickle import HIGHEST_PROTOCOL, loads, dumps
from pickletools import optimize
from time import time as now
from contextlib import contextmanager
from math import log, log10, ceil

UNIT_CLUSTERING = 3

def get_unit(i):
    l = ceil(log10(i))
    shift = ceil(log(i, UNIT_CLUSTERING)) * -1

    units = { 1: ('s', 1),
             -0: ('ms', 1_000),
             -1: ('ms', 1_000),
             -2: ('ms', 1_000),
             -3: ('us', 1_000_000),
             -4: ('us', 1_000_000),
             -5: ('us', 1_000_000),
             -6: ('ns', 1_000_000_000),
             -7: ('ns', 1_000_000_000),
             -8: ('ns', 1_000_000_000),
             
             -9: ('xx', 1_000_000_000),
             -10: ('xx', 1_000_000_000),
             -11: ('xx', 1_000_000_000),
            }
    unit, shift = units.get(l, units[1])

    return i * shift, unit

@contextmanager
def period(name):
    start = now()
    yield
    end = now()

    time = end - start

    time, unit = get_unit(time)
    
    print(f"{name} {time:.1F} {unit}")

print("=" * 24)
DATA = (1,2,3,4,5)
print("Data:", DATA)
print("-" * 24)

for i in range(1, HIGHEST_PROTOCOL + 1):
    from time import sleep
    with period(f'Pickling @ {i} (Optimized)'):
        result = dumps(DATA)
        optimize(result)
    with period(f'Pickling @ {i}            '):
        result = dumps(DATA)
    with period(f'UnPickling @ {i}          '):
        loads(result)
    print("-" * 24)
    
