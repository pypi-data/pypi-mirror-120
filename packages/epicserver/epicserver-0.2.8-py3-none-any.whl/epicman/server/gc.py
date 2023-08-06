#!/usr/bin/env python3

from contextlib import contextmanager
from time import monotonic_ns as now
import gc
from enum import IntEnum

class GENERATION(IntEnum):
    NEW=0
    YOUNG=1
    OLD=2

class Logger():
    def __init__(self, log):
        self.log = log
        
    def install(self):
        gc.callbacks.append(logger)

    def __call__(self, phase, info):
        pass

    @contextmanager
    def pause_gc(self):
        self.log("Disabling GC")
        start = now()
        gc.disable()
        try:
            yield
        finally:
            self.log("Enableing GC")
            gc.enable()
        end = now()
        period = end - start
        self.log(f"Garbage collection enabled, disabled for {period}ns {start}->{end}")

        start = now()
        gc.collect(GENERATION.YOUNG)
        end = now()
        period = end - start
        self.log(f"Performing GC of generation {generation}, Time Taken={period}ns")
