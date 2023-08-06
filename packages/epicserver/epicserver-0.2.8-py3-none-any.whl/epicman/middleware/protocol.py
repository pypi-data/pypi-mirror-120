#!/usr/bin/python3

from struct import Struct

# * Buffer incomming recived_data
# * Slice up buffer acording to packetization
# * Convert packet to a python object

READ_SIZE = 4096

class Packetize():
    header = Struct('<H')
    def __init__(self, conn):
        self.buffer = b''
        self.conn = conn
        
    async def recv(self, timeout=0) -> bytes:
        while True:
            buffer = self.buffer
            while len(buffer) < self.header.size:
                data = await self.conn.recv(READ_SIZE, timeout=timeout)
                if not data:
                    raise ConnectionError('Remote end is disconnected')
                buffer += data
            
            packet_len = self.header.unpack_from(buffer)[0]
            buffer = buffer[self.header.size:]

            while len(buffer) < packet_len:
                data = await self.conn.recv(READ_SIZE, timeout=timeout)
                if not data:
                    raise ConnectionError('Remote end is disconnected')
                buffer += data

            self.buffer = buffer[packet_len:]
            buffer = buffer[:packet_len]

            yield buffer

    async def send(self, data: bytes, timeout=0):
        header = self.header.pack(len(data))
        return await self.conn.sendall(header + data) - len(header)
