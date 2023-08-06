#!/usr/bin/env python

from epicman.middleware.protocol import Packetize
from epicman.server import MainLoop
from epicman.objects import callable_entity

import pytest
import sys

class conn():
    _buffer = b''
    def __init__(self, data = b''):
        self._buffer = data

    async def recv(self, size, timeout=0):
        return self._buffer

    async def sendall(self, data, timeout=0):
        self._buffer += data
        return len(data)

def roundtrip(val):
    async def inner():
        packetizer = Packetize(conn())
        await packetizer.send(val)
        async for packet in packetizer.recv():
            assert val == packet
            break
        sys.exit()
    return inner

@pytest.mark.parametrize('data', [
    b"",
    b"a",
    b"ddddddddddddddddddddddddddddddddddddddd",
    b"d" * 1500,
    b"d" * 64_000,
    ])
def test_roundtrip(data):
    main_loop = MainLoop({})
    with pytest.raises(SystemExit):
        main_loop.run_forever([roundtrip(data)])
