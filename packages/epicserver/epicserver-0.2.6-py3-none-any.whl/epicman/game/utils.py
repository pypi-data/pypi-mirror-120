#!/usr/bin/env python3

from ..server.syscalls import *

from contextvars import ContextVar
from contextlib import suppress
from functools import wraps
from typing import Callable, NamedTuple, Any

from .. import running_task


class EntityProxy():
    def __init__(self, base_class):
        self.base_class = base_class

    def __getitem__(self, key):
        obj = self.base_class(key)
        return obj

    def __repr__(self) -> str:
        return f'<EntityProxy {self.base_class.__name__}>'

    def __rmatmul__(self, other):
        return self[other]


# TODO: wrap this up with error propergation
def remote_call(func):
    @wraps(func)
    async def wrapped_remote_call(self, *args, timeout=0, **kwargs):
        await TASK_SEND(self, (func.__name__, args, kwargs))
        return await TASK_RECV(timeout=timeout)
    wrapped_remote_call._implementation = func
    return wrapped_remote_call

def remote_msg(func):
    @wraps(func)
    async def wrapped_remote_call(self, *args, **kwargs):
        await TASK_SEND(self, (func.__name__, args, kwargs))
    wrapped_remote_call._implementation = func
    return wrapped_remote_call

def remote_stream(func):
    # V V V CALLED FUNCTION
    @wraps(func)
    async def wrapped_implementation(self, addr, *args, timeout=0, **kwargs):
        try:
            async for val in func(self, *args, **kwargs):
                await TASK_SEND(addr, (val, None))
        except Exception as err:
            await TASK_SEND(addr, (None, err))
            raise
        await TASK_SEND(addr, (None, StopAsyncIteration()))

    # V V V CALLER FUNCTION
    @wraps(func)
    async def wrapped_caller(self, *args, timeout=0, **kwargs):
        calling_task = running_task.get()
        await TASK_SEND(self, (func.__name__, (calling_task,) + args, kwargs))
        while True:
            val, exc = await TASK_RECV(timeout=timeout)
            if exc is not None:
                if isinstance(exc, StopAsyncIteration):
                    break
                raise exc
            yield val
    wrapped_caller._implementation = wrapped_implementation

    return wrapped_caller
#
#Address = Tuple[int, str, int]
#Addresses = List[Address]
#async def multi_connect(addrs: Addresses, typ=socket.SOCK_STREAM):
#    conns = []
#    epoll = Epoll()
#    for AF, host, port in addrs:
#        s = socket.socket(AF, typ)
##        conns.append(AsyncSocket(s))
#        s.setblocking(False)
#        conns.append(s)
#        epoll.register(READ, conn)
#
#    for conn, addr in zip(conns, addrs):
#        conn.connect(addr)
#
#    await SYSCALL_READ(epoll, 0)
#    # B-UG: this may raise a type error is select is empty
#    file, event =  epoll.select()[0]
#    established = file
#
#    for conn in conns:
#        if conn is not established:
#            conn.close()
#    
#    epoll.close()
#    return established

def callable_entity(func):
    d = {}
    # we wrap the func in a staticmethod so it does not get the 
    # unexpected 'self' arg from being a class member
    d['__call__'] = staticmethod(func)
    d['__module__'] = func.__module__
    new_cls = type(func.__name__, (Entity,), d)
    proxy = EntityProxy(new_cls)
    return proxy

class Entity():
    id: str
    def __init__(self, id):
        self.id = id

    @remote_call
    def reset(self):
        pass

    def _save(self) -> dict:
        pass
        
    @classmethod
    def _restore(cls, **kwargs):
        pass

    async def __call__(self, *args, **kwargs):
        while True:
            func_name, args, kwargs = await TASK_RECV()
            func = getattr(self, func_name)
            await func._implementation(self, *args, **kwargs)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}:{self.id}"
    def __repr__(self) -> str:
        return f"<Entity {self.__class__.__name__}:{self.id}>"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return NotImplemented
    
    def __hash__(self):
        return hash(self.id)

    def __epic_id__(self):
        return EntityAddr(self.__class__, self.id)


class EntityAddr(NamedTuple):
    namespace: Entity
    instance: Any
