#!/usr/bin/env python3
"""This module is a stub module (does not rely on code from epicman) for the 
syscalls for Mainloop <> Entity interaction. The behavior of each syscall is
defined in the mainloop with minor overrides (eg THREAD_SLEEP) where strictly 
required
"""

#### NOTE: All syscalls should be immutable ####

from typing import Optional, Union, Any, Iterable, Tuple
from dataclasses import dataclass
from socket import socket
import sys

# TODO: make this the default for timeout field and kill off conditional in main loop
# We halve sys.maxsize so we can add a unix time to the delay without overflow
# into a Largenum. There may be edge cases such as on 32bit arch's where unix
# time as of 2021 is 31bits in length in which case the only resonable case is 
# to overflow to a larger representitive type
MAX_DELAY = sys.maxsize//2

# Types
FileDescriptor = Union[int, socket]


class GameEnd(Exception):
    pass


class ServerUpdate(Exception):
    @property
    def msg(self):
        return self.args[0]


@dataclass
class SYSCALL():
    def __await__(self):
        ret = yield self
        return ret


@dataclass
class SOCK_ACCEPT(SYSCALL):
    file: FileDescriptor
    timeout: float = 0


@dataclass
class SOCK_CONNECT1(SYSCALL):
    file: FileDescriptor
    addr: tuple
    timeout: float = 0


@dataclass
class SOCK_CONNECT2(SYSCALL):
    file: FileDescriptor
    addr: tuple
    timeout: float = 0


@dataclass
class SOCK_RECV(SYSCALL):
    file: FileDescriptor
    size: int
    flags: int = 0
    timeout: float = 0


@dataclass
class SOCK_RECVFROM(SYSCALL):
    file: FileDescriptor
    size: int
    flags: int = 0
    timeout: float = 0


@dataclass
class SOCK_SEND(SYSCALL):
    file: FileDescriptor
    data: bytes
    flags: int = 0
    timeout: float = 0

@dataclass
class SOCK_SENDMSG(SYSCALL):
    file: FileDescriptor
    buffers: Iterable[bytes]
    ancdata: Iterable[Tuple[int, int, Any]]
    flags: int = 0
    address: Optional[tuple] = None
    timeout: float = 0

@dataclass 
class SOCK_SENDTO(SYSCALL):
    file: FileDescriptor
    data: bytes
    address: tuple
    flags: int = 0
    timeout: float = 0


@dataclass
class FILE_READ(SYSCALL):
    file: FileDescriptor
    size: int
    timeout: float = 0


@dataclass
class FILE_WRITE(SYSCALL):
    file: FileDescriptor
    data: bytes
    timeout: float = 0


@dataclass
class ENTITY_CALL(SYSCALL):
    addr: Any
    method: str
    args: tuple
    kwargs: dict
    timeout: float = 0


@dataclass
class ENTITY_SPAWN(SYSCALL):
    addr: Any
    method: str
    args: tuple
    kwargs: dict
    timeout: float = 0


@dataclass
class FUTURE_NOTIFY(SYSCALL):
    future: Any
    timeout: float = 0


@dataclass
class FUTURE_WAIT(SYSCALL):
    future: Any
    timeout: float = 0


@dataclass
class THREAD_SLEEP(SYSCALL):
    timeout: float = 0

    def __await__(self):
        ret = None
        try:
            ret = yield self
        except TimeoutError:
            pass
        return ret


@dataclass
class GET_NAME(SYSCALL):
    name: str
    timeout: float = 0


@dataclass
class CHECKPOINT(SYSCALL):
    state: Optional[dict] = None

    # due to implementation details this
    # can never be canceled. the backend would block
    # timeout would be exceeded and then the cancel
    # would overwright the CHECKPOINT syscall return
    # value
    @property
    def timeout(self):
        return 0


__all__ = ["GameEnd",
           "ServerUpdate",
           "SOCK_RECV",
           "SOCK_RECVFROM",
           "SOCK_SEND",
           "SOCK_SENDMSG",
           "SOCK_SENDTO",
           "SOCK_ACCEPT",
           "SOCK_CONNECT1",
           "SOCK_CONNECT2",
           "FILE_READ",
           "FILE_WRITE",
           "ENTITY_CALL",
           "ENTITY_SPAWN",
           "THREAD_SLEEP",
           "FUTURE_WAIT",
           "FUTURE_NOTIFY",
           "GET_NAME",
           "CHECKPOINT",
           ]
