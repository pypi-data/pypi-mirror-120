#!/usr/bin/env python3

from time import time as now

from ..syscalls import SOCK_CONNECT1, SOCK_CONNECT2, SOCK_ACCEPT
from ..syscalls import SOCK_RECV, SOCK_RECVFROM
from ..syscalls import SOCK_SEND, SOCK_SENDMSG, SOCK_SENDTO

from typing import Union

import socket
import errno
import sys

from ctypes import c_uint8, c_uint32, c_uint64
from ctypes import get_errno, sizeof, pointer
from ctypes import Structure, CDLL

from ipaddress import ip_address

_libc = CDLL("libc.so.6", use_errno=True)
_raw_getsockopt = _libc.getsockopt


def async_socket(*args, **kwargs):
    sock = socket.socket(*args, **kwargs)
    sock = AsyncSocket(sock)

    return sock


class AsyncSocket():
    def __init__(self, sock):
        self._read_sock = sock
        # our callbacks in the mainloop are keyed by fd and not fd, event_type
        # hence we need a way to detirmine reads vs writes
        self._write_sock = sock.dup()
        sock.setblocking(False)

    async def accept(self):
        conn, addr = await SOCK_ACCEPT(self._read_sock)
        ip, *extra = addr
        ip = ip_address(ip)
        # we need a tuple as the return value as we may use this as a 
        # dict key and therefore cant be mutable
        extra = tuple(extra)
        conn = AsyncSocket(conn)
        return conn, ((ip,) + extra)

    async def recv(self, size, flags=0, *, timeout=0):
        data = await SOCK_RECV(self._read_sock, size, flags=flags, timeout=timeout)
        return data

    async def recv_into(self, buffer, nbytes=None, flags=0, *, timeout=0) -> int:
        raise NotImplementedError()

    async def recvfrom(self, buffersize: int, flags=0, *, timeout=0):
        return await SOCK_RECVFROM(self._read_sock, buffersize, flags, timeout=timeout)

    async def recvfrom_into(self, buffer, nbytes=None, flags=0, *, timeout=0):
        raise NotImplementedError()

    async def recvmsg(self, bufsize, ancbufsize=None, flags=0, *, timeout=0):
        raise NotImplementedError()

    async def recvmsg_into(self, buffers, ancbufsize=None, flags=0, *, timeout=0):
        raise NotImplementedError()

    async def send(self, data, flags=0, *, timeout=0) -> int:
        return await SOCK_SEND(self._write_sock, data, flags=flags, timeout=timeout)

    async def sendall(self, data, flags=0, *, timeout=0) -> int:
        expiry_time = now() + timeout
        total_sent = 0
        while total_sent < len(data):
            delta = now() - expiry_time
            sent = await self.send(data[total_sent:], timeout=delta)
            total_sent += sent
        
        return total_sent

    async def sendto(self, data: bytes, arg1, arg2=None, timeout=0) -> int:
        flags, address = 0, arg1
        if arg2:
            flags, address = arg1, arg2
        return await SOCK_SENDTO(self._write_sock, data, address, flags)

    async def sendfile(self, file, offset: int = None, count: int = sys.maxsize) -> int:
        CHUNK_SIZE = 64 * 1024

        if self._write_sock.type != socket.SOCK_STREAM:
            raise ValueError('only SOCK_STREAM type sockets are supported')

        if offset is not None:
            file.seek(offset)
        total_sent = 0
        for chunk in iter(lambda: file.read(CHUNK_SIZE), b''):
            sent = await self.sendall(chunk)
            total_sent += sent
            if sent == 0:
                break
            if total_sent >= count:
                break

        return total_sent

    async def sendmsg(self, buffers, ancdata=(), flags=0, address=None, timeout=0) -> int:
        return await SOCK_SENDMSG(self._write_sock, buffers, ancdata, flags, address, timeout=timeout)

    async def connect(self, addr, *, timeout=0):
        old_timeout = self._write_sock.gettimeout()
        try:
            self._write_sock.settimeout(timeout)
            # kick off the inital connection
            await SOCK_CONNECT1(self._write_sock, addr)
            # wait for read, exception communicates issue
            await SOCK_CONNECT2(self._write_sock, addr)
        finally:
            self._write_sock.settimeout(old_timeout)

    async def connect_ex(self, addr, *, timeout=0) -> int:
        raise NotImplementedError()

    def setsockopt(self, *args, **kwargs):
        return self._read_sock.setsockopt(*args, **kwargs)

    def getsockopt(self, *args, **kwargs):
        return self._read_sock.getsockopt(*args, **kwargs)

    def listen(self, backlog=None):
        if backlog:
            self._read_sock.listen(backlog)
        else:
            self._read_sock.listen()

    def bind(self, addr):
        self._read_sock.bind(addr)

    def shutdown(self, value):
        self._read_sock.shutdown(value)

    def close(self):
        self._read_sock.close()
        self._write_sock.close()

    def getpeername(self):
        addr, *extra = self._read_sock.getpeername()
        addr = ip_address(addr)
        # we need a tuple as the return value as we may use this as a 
        # dict key and therefore cant be mutable
        return (addr,) + tuple(extra)

    def getsockname(self):
        addr, *extra = self._read_sock.getsockname()
        addr = ip_address(addr)
        # we need a tuple as the return value as we may use this as a 
        # dict key and therefore cant be mutable
        return (addr,) + tuple(extra)


class TCP_Info(Structure):
    _fields_ = [
        ("state",           c_uint8),
        ("ca_state",        c_uint8),
        ("retransmits",     c_uint8),
        ("probes",          c_uint8),
        ("backoff",         c_uint8),
        ("options",         c_uint8),
        ("snd_wscale",      c_uint8),
        ("delivery_rate_app_limited", c_uint8),

        ("rto",             c_uint32),
        ("ato",             c_uint32),
        ("snd_mss",         c_uint32),
        ("rcv_mss",         c_uint32),

        ("unacked",         c_uint32),
        ("sacked",          c_uint32),
        ("lost",            c_uint32),
        ("retrans",         c_uint32),
        ("fackets",         c_uint32),

        # Times.
        ("last_data_sent",  c_uint32),
        ("last_ack_sent",   c_uint32),
        ("last_data_recv",  c_uint32),
        ("last_ack_recv",   c_uint32),

        # Metrics.
        ("pmtu",            c_uint32),
        ("rcv_ssthresh",    c_uint32),
        ("rtt",             c_uint32),
        ("rttvar",          c_uint32),
        ("snd_ssthresh",    c_uint32),
        ("snd_cwnd",        c_uint32),
        ("advmss",          c_uint32),
        ("reordering",      c_uint32),

        ("rcv_rtt",         c_uint32),
        ("rcv_space",       c_uint32),

        ("total_retrans",   c_uint32),

        ("pacing_rate",     c_uint64),
        ("max_pacing_rate", c_uint64),
        ("bytes_acked",     c_uint64),  # RFC4898 tcpEStatsAppHCThruOctetsAcked
        ("bytes_received",  c_uint64),  # RFC4898 tcpEStatsAppHCThruOctetsReceived
        ("segs_out",        c_uint32),  # RFC4898 tcpEStatsPerfSegsOut
        ("segs_in",         c_uint32),  # RFC4898 tcpEStatsPerfSegsIn

        ("notsent_bytes",   c_uint32),
        ("min_rtt",         c_uint32),
        ("data_segs_in",    c_uint32),  # RFC4898 tcpEStatsDataSegsIn
        ("data_segs_out",   c_uint32),  # RFC4898 tcpEStatsDataSegsOut

        ("delivery_rate",   c_uint64),

        ("busy_time",       c_uint64),  # Time (usec) busy sending data
        ("rwnd_limited",    c_uint64),  # Time (usec) limited by receive window
        ("sndbuf_limited",  c_uint64),  # Time (usec) limited by send buffer

        ("delivered",       c_uint32),
        ("delivered_ce",    c_uint32),

        ("bytes_sent",      c_uint64),  # RFC4898 tcpEStatsPerfHCDataOctetsOut
        ("bytes_retrans",   c_uint64),  # RFC4898 tcpEStatsPerfOctetsRetrans
        ("dsack_dups",      c_uint32),  # RFC4898 tcpEStatsStackDSACKDups
        ("reord_seen",      c_uint32),  # reordering events seen
        ]


def get_tcp_info(s: Union[socket.socket, int]) -> TCP_Info:
    if hasattr(s, 'fileno'):
        s = s.fileno()
    elif not isinstance(s, int):
        try:
            s = int(s)
        except TypeError as err:
            raise ValueError('provided socket cannot be turned into a file descriptor') from err

    info = TCP_Info()
    info_len = c_uint32(sizeof(info))

    ret = _raw_getsockopt(s, socket.IPPROTO_TCP, socket.TCP_INFO, pointer(info), pointer(info_len))

    if ret != 0:
        err_code = get_errno()
        if err_code == errno.EBADF:
            raise OSError(err_code, 'Bad File Descriptor')
        elif err_code == errno.ENOTSUP:
            raise OSError(err_code, 'File Descriptor does not refer to a TCP socket')
        elif err_code == errno.ENOTSOCK:
            raise OSError(err_code, 'File Descriptor does not refer to a socket')
        elif err_code == errno.ENOPROTOOPT:
            raise OSError(err_code, 'Protocol option not avalible on this socket')
        else:
            raise OSError(err_code, 'Unknown Error')

    return info
