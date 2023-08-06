#!/usr/bin/env python3

from typing import NamedTuple, Callable, Union, Any
from typing import NamedTuple, List
from socket import socket

# Types
FileDescriptor = Union[int, socket]


class GameEnd(Exception): pass
class ServerUpdate(Exception):
    @property
    def msg(self):
        return self.args[0]


class TaskID(NamedTuple):
    namespace: Callable
    id: int

# TODO: swap out NamedTuples with dataclasses
class SOCK_ACCEPT(NamedTuple):
    file: FileDescriptor
    timeout: float = 0
    def __await__(self):
        ret = yield self
        return ret
class SOCK_CONNECT1(NamedTuple):
    file: FileDescriptor
    addr: tuple
    timeout: float = 0
    def __await__(self):
        ret = yield self
        return ret
class SOCK_CONNECT2(NamedTuple):
    file: FileDescriptor
    addr: tuple
    timeout: float = 0
    def __await__(self):
        ret = yield self
        return ret
class SOCK_RECV(NamedTuple):
    file: FileDescriptor
    size: int
    timeout: float = 0
    def __await__(self):
        ret = yield self
        return ret
class SOCK_RECVFROM(NamedTuple):
    file: FileDescriptor
    size: int
    flags: int = 0
    timeout: float = 0
    def __await__(self):
        ret = yield self
        return ret
class SOCK_SEND(NamedTuple):
    file: FileDescriptor
    data: bytes
    timeout: float = 0
    def __await__(self):
        ret = yield self
        return ret
class SOCK_SENDTO(NamedTuple):
    file: FileDescriptor
    data: bytes
    flags: int
    address: tuple
    timeout: float = 0
    def __await__(self):
        ret = yield self
        return ret
class FILE_READ(NamedTuple):
    file: FileDescriptor
    size: int
    timeout: float = 0
    def __await__(self):
        ret = yield self
        return ret
class FILE_WRITE(NamedTuple):
    file: FileDescriptor
    data: bytes
    timeout: float = 0
    def __await__(self):
        ret = yield self
        return ret
class TASK_SEND(NamedTuple):
    dst_task: TaskID
    msg: Any
    timeout: float = 0
    def __await__(self):
        ret = yield self
        return ret
class TASK_RECV(NamedTuple):
    timeout: float = 0
    def __await__(self):
        ret = yield self
        return ret
class TASK_SLEEP(NamedTuple):
    timeout: float = 0
    def __await__(self):
        try:
            ret = yield self
        except TimeoutError:
            pass
        return
class GET_NAME(NamedTuple):
    name: str
    timeout: float = 0
    def __await__(self) -> List[str]:
        ret = yield self
        return ret
class SERIALIZE(NamedTuple):
    args: tuple
    kwargs: dict
    timeout: float = 0


__all__ = ["GameEnd",
           "ServerUpdate", 
           "TaskID", 
           "SOCK_RECV", 
           "SOCK_RECVFROM", 
           "SOCK_SEND", 
           "SOCK_SENDTO", 
           "SOCK_ACCEPT", 
           "SOCK_CONNECT1", 
           "SOCK_CONNECT2", 
           "FILE_READ", 
           "FILE_WRITE", 
           "TASK_SEND", 
           "TASK_RECV", 
           "TASK_SLEEP", 
           "GET_NAME", 
           "SERIALIZE",
          ]
