#!/usr/bin/env python3

from ...game.socket import AsyncSocket

from dns.asyncresolver import resolve, Resolver
from dns.asyncquery import udp, tcp
import dns.message

from functools import wraps
import socket

import dns._asyncbackend
import dns.exception
import dns.inet


# for brevity
_lltuple = dns.inet.low_level_address_tuple


def raise_timeout(func):
    @wraps(func)
    def inner(*args, timeout=0, **kwargs):
        try:
            return func(*args, **kwargs)
        except Timeout as err:
            raise dns.exception.Timeout(timeout=timeout) from err
    return inner


class DNSSocket(dns._asyncbackend.DatagramSocket):
    def __init__(self, socket):
        self.socket = socket
        self.family = socket._sock.family

    @raise_timeout
    async def sendto(self, what, destination, timeout):
        return await self.socket.sendto(what, destination)

    @raise_timeout
    async def sendall(self, what, timeout):
        return await self.socket.sendall(what, timeout=timeout)

    @raise_timeout
    async def recvfrom(self, size, timeout):
        return await self.socket.recvfrom(size)

    @raise_timeout
    async def recv(self, size, timeout):
        return await self.socket.recv(size, timeout=timeout)

    async def close(self):
        self.socket.close()

    async def getpeername(self):
        return self.socket.getpeername()

    async def getsockname(self):
        return self.socket.getsockname()


class Backend(dns._asyncbackend.Backend):
    def name(self):
        return 'epicman'

    async def make_socket(self, af, socktype, proto=0, source=None,
                          destination=None, timeout=0,
                          ssl_context=None, server_hostname=None):
        if ssl_context:
            raise NotImplementedError('No SSL support at this time')

        s = socket.socket(af, socktype, proto)
        s = AsyncSocket(s)
        try:
            if source:
                s.bind(_lltuple(source, af))
            if socktype == socket.SOCK_STREAM:
                await s.connect(_lltuple(destination, af), timeout=timeout)
        except Exception:  # pragma: no cover
            s.close()
            raise
        return DNSSocket(s)

    async def sleep(self, interval):
        await TASK_SLEEP(interval)


def install():
    import dns.asyncbackend
    backend = Backend()
    dns.asyncbackend._backends['epicman.server'] = backend
    dns.asyncbackend._default_backend = backend
