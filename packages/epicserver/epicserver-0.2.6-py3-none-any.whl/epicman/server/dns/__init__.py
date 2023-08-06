#!/usr/bin/env python3

from epicman.game.utils import EntityProxy, Entity, remote_call
from ..syscalls import *

from .dnspython import install, Resolver
from dns.rdatatype import *

from time import time as now

install()
r = Resolver()

@EntityProxy
class DNSCache(Entity):
    record = None
    expiration = 0

    async def _resolve(self):
        host, typ = self.__epic_id__()[1]

        record = await r.resolve(host, typ)
        self.expiration = record.expiration
        self.record  = record.rrset

    @remote_call
    async def resolve(self, reply):
        if self.expiration < now():
            await self._resolve()
        await TASK_SEND(reply, self.record)
