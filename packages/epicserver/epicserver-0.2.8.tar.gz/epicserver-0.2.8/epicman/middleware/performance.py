#!/usr/bin/env python3


LATENCY_PATH = "/dev/cpu_dma_latency"
LATENCY_VALUE = b"0x00000000"


class Performance():
    latency_file = None

    def set_low_latency():
        # Prevent processor going into C-STATE idle
        # this is equivlent to kernel args cstate=1 and idle=0
        # but allows us to adjust this at run time
        f = open(LATENCY_PATH)
        f.write(LATENCY_VALUE)

        self.latency_file = f
