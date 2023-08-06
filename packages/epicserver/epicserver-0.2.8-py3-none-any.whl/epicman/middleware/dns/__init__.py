#!/usr/bin/env python3

from ...objects import EntityProxy, Entity, remote_call

from .dnspython import install, Resolver
from dns.rdatatype import *  # noqa: F401,F403

from time import time as now

install()
r = Resolver()


# TODO: work out how we can go back to a decorator
class _ClusterDNSCache(Entity):
    record = None
    expiration = 0

    async def _resolve(self):
        host, typ = self.instance

        record = await r.resolve(host, typ)
        self.expiration = record.expiration
        self.record = record.rrset

    @remote_call
    async def resolve(self):
        if self.expiration < now():
            await self._resolve()
        return self.record
ClusterDNSCache = EntityProxy(_ClusterDNSCache)


class _LocalDNSCache(_ClusterDNSCache):
    _local_only = True
# TODO: work out how we can go back to a decorator
LocalDNSCache = EntityProxy(_LocalDNSCache)


DNSCache = LocalDNSCache
