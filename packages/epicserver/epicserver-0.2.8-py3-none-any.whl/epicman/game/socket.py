#!/usr/bin/env python3

from ..server.syscalls import *
from socket import socket

class AsyncSocket():
    def __init__(self, sock):
        self._sock = sock
        sock.setblocking(False)
        
    async def accept(self):
        # TODO: transform fd/connection into async socket
        conn = await SOCK_ACCEPT(self._sock)
        return conn
        
    # TODO: Implement flags in syscall
    async def recv(self, size, flags=0, *, timeout=0):
        data = await SOCK_RECV(self._sock, size, timeout=timeout)
        return data

    async def recv_into(self, buffer, nbytes=None, flags=0, *, timeout=0) -> int:
        raise NotImplemented()

    async def recvfrom(self, buffersize: int, flags=0, *, timeout=0):
        return await SOCK_RECVFROM(self._sock, buffersize, flags, timeout=timeout)

    async def recvfrom_into(self, buffer, nbytes=None, flags=0, *, timeout=0):
        raise NotImplemented()

    async def recvmsg(self, bufsize, ancbufsize=None, flags=0, *, timeout=0):
        raise NotImplemented()

    async def recvmsg_into(self, buffers, ancbufsize=None, flags=0, *, timeout=0):
        raise NotImplemented()

    # TODO: Implement flags in syscall
    async def send(self, data, flags=0, *, timeout=0) -> int:
        return await SOCK_SEND(self._sock, data, timeout=timeout)

    from time import time as now
    async def sendall(self, data, flags=0, *, timeout=0) -> int:
        expiry_time = now() + timeout
        sent = await self.send(data, timeout=timeout)
        total_sent = sent
        while sent and total_sent < len(data):
            sent = await self.send(data[sent:], timeout=now() - expiry_time)
            total_sent += sent

        return total_sent

    async def sendto(self, data: bytes, arg1, arg2=None) -> int:
        flags, address = 0, arg1
        if arg2:
            flags, address = arg1, arg2
        return await SOCK_SENDTO(self._sock, data, flags, address)
        
    async def sendfile(self, file, offset: int=None, count: int=None) -> int:
        CHUNK_SIZE=64*1024
        
        if self._sock.type != socket.SOCK_STREAM:
            raise ValueError('only SOCK_STREAM type sockets are supported')

        if offset is not None:
            file.seek(offset)
        total_sent = 0
        # TODO: implement count support to limit outgoing bytes
        for chunk in iter(lambda: file.read(CHUNK_SIZE), b''):
            sent = await self.sendall(chunk)
            total_sent += sent
            if sent == 0:
                break

        return total_sent

    async def sendmsg(self, buffers, ancdata=None, flags=None, address=None) -> int:
        raise NotImplemented()
        
    async def connect(self, addr, *, timeout=0):
        old_timeout = self._sock.gettimeout()
        try:
            self._sock.settimeout(timeout)
            # kick off the inital connection
            await SOCK_CONNECT1(self._sock, addr)
            # wait for read, exception communicates issue
            await SOCK_CONNECT2(self._sock, addr)
        finally:
            self._sock.settimeout(old_timeout)
    async def connect_ex(self, addr, *, timeout=0) -> int:
        raise NotImplemented()

    def listen(backlog=None):
        if backlog:
            self._sock.listen(backlog)
        else:
            self._sock.listen()

    def bind(self, addr):
        self._sock.bind(addr)

    def shutdown(self, value):
        self._sock.shutdown(value)

    def close(self):
        self._sock.close()

    def getpeername(self):
        return self._sock.getpeername()

    def getsockname(self):
        return self._sock.getsockname()
