#!/usr/bin/env python3

from .constants import hash_algo as routing_hash_algo
from .syscalls import ENTITY_CALL, ENTITY_SPAWN, FUTURE_WAIT, FUTURE_NOTIFY, SYSCALL, CHECKPOINT

from typing import NamedTuple, Type, Callable, Coroutine, AsyncIterator, List, Any, Union
from functools import wraps


Number = Union[float, int]

class EntityProxy():
    def __init__(self, base_class):
        base_class._constructor = self
        self.base_class = base_class

    def __getitem__(self, key):
        obj = self.base_class(key)
        return obj

    def __repr__(self) -> str:
        return f'<EntityProxy {self.base_class.__name__}>'

    def __rmatmul__(self, other):
        return self[other]


def remote_call(func: Callable) -> Callable:
    @wraps(func)
    async def wrapped_caller(self, *args, timeout: Number=0, **kwargs):
        ret = await ENTITY_CALL(self, func, args, kwargs, timeout=timeout)
        return ret
    wrapped_caller._implementation = func

    return wrapped_caller

def remote_spawn(func: Callable) -> Callable:
    @wraps(func)
    async def wrapped_caller(self, *args, timeout: Number=0, **kwargs):
        ret = await ENTITY_SPAWN(self, func, args, kwargs, timeout=timeout)
        return ret
    wrapped_caller._implementation = func

    return wrapped_caller


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


def callable_entity(func: Callable[[Any], Coroutine[SYSCALL, Any, Any]]):
    # we wrap the func in a staticmethod so it does not get the
    # unexpected 'self' arg from being a class member
    class func_backed_entity(Entity):
        def _activate(self):
            self.state = {}

        @remote_call
        @wraps(func)
        async def __call__(self, *args, **kwargs):
            state = {**self.state, **kwargs}

            ret = await func(*args, **state)

            return ret

        @classmethod
        def _restore(cls, instance, state):
            o = cls(instance)
            o.state = state
            return o

        def _save(self):
            return None

    func_backed_entity.__module__ = func.__module__
    func_backed_entity.__name__ = func.__name__
    # as we use @wrap on __call__ its name gets changed to match `func`
    # @remote_call introspects this and attemtps to invoke the wrong name
    # ie func.__name__ rather than func_backed_entity.__call__
    # this next line dummies up an entry to that calling it the incorrect
    # way works AND so that Threads display the invoked function name 
    # correctly in the logs
    setattr(func_backed_entity, func.__name__, func_backed_entity.__call__)
    
    proxy = EntityProxy(func_backed_entity)

    return proxy


class Entity():
    instance: str
    _persist: List[str] = []
    _only_local = False

    def __init__(self, instance):
        self.instance = instance

    def __reduce__(self):
        return (self._constructor.__getitem__, (self.instance,))

    def _activate(self):
        """Hook to allow users to set the object to its default state"""
        pass

    def _deactivate(self):
        """Hook to allow users to implement cleanup actions before a Entity is GC'd"""
        pass

    @remote_call
    async def reset(self):
        if hasattr(self, '__slots__'):
            for slot in self.__slots__:
                delattr(self, slot)
        else:
            self.__dict__.clear()

        self._activate()

        await CHECKPOINT(state={})

    def _save(self) -> dict:
        state = {}
        for attr in self._persist:
            state[attr] = getattr(self, attr)
        return state

    @classmethod
    def _restore(cls, instance, state):
        obj = cls.__new__(cls)
        obj.instance = instance
        for attr, val in state.items():
            setattr(obj, attr, val)

        return obj

    def __str__(self) -> str:
        instance = str(self.instance)
        if instance.startswith('('):
            instance = instance[1:-1]
        return f"{self.__class__.__name__}:{instance}"

    def __repr__(self) -> str:
        return f"<Entity {self.__class__.__name__}:{self.instance}>"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.instance == other.instance
        return NotImplemented

    def __hash__(self):
        return hash((self.__class__, self.instance))


class Lock():
    async def wait(self, timeout=0):
        await FUTURE_WAIT(self, timeout=timeout)
        
    async def notify(self):
        await FUTURE_NOTIFY(self)


class Future():
    def __init__(self):
        self._value = None
        self._value_set = False
        self._lock = Lock()

    async def wait(self, timeout=0):
        await self._lock.wait(timeout=timeout)
        return self._value

    async def set_value(self, value):
        self._value = value
        self._value_set = True
        await self._lock.notify()

    def get_value(self):
        if not self._value_set:
            raise ValueError("Value has not yet been set")
        return self._value


class Queue():
    def __init__(self):
        self._list = []
        self._lock = Lock()

    async def append(self, val):
        self._list.append(val)
        await self._lock.notify()

    async def pop(self, index=-1, timeout=0):
        while not self._list:
            await self._lock.wait(timeout=timeout)

        return self._list.pop(index)

    def __iter__(self):
        return iter(self._list)
