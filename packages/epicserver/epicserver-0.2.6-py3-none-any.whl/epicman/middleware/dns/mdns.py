#!/usr/bin/env python3

from ...objects import EntityProxy, Entity
from ...objects import remote_call

from ...logging import log

from ...helpers.file import cmd_wrapper

from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import NamedTuple, Union

from functools import wraps
from enum import Enum

import socket
import uuid


DEFAULT_NAME = socket.gethostname()
SERVICE_TYPE = '_epic._tcp'
publish_cmd = ["avahi-publish-service", "-v", "-f", DEFAULT_NAME, SERVICE_TYPE]
discover_cmd = ["avahi-browse", "-r", "-p", "-f", "--no-db-lookup", SERVICE_TYPE]


class Action(Enum):
    ADD = '+'
    UPDATE = '='
    DELETE = '-'


SEP = ';'


class Update(NamedTuple):
    action: Action
    iface: str
    service: str
    name: str
    domain: str
    hostname: str = None
    address: Union[IPv4Address, IPv6Address] = None
    port: int = None
    metadata: dict = {}


def error(err, msg):
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except err:
                log.error(msg)
                raise
        return inner
    return outer


def decode_hostname(s):
    frags = s.split('\\')
    out = []
    for i in range(len(frags) - 1):
        out.append(frags[i])
        char = frags[i + 1][:3]
        char = chr(int(char))
        out.append(char)
        frags[i + 1] = frags[i + 1][3:]
    out.append(frags[-1])
    # no substituion performed so no data in out
    if not out:
        out = frags

    return ''.join(out)


def parse(line):
    if line.count(SEP) == 5:
        line = line.split(SEP)
    else:
        line = line.split(SEP, maxsplit=9)

    action = Action(line[0])
    iface = line[1]
    name = decode_hostname(line[3])
    service = line[4].rsplit('.', maxsplit=1)
    domain = line[5]

    kwargs = {}
    if len(line) > 6:
        kwargs['hostname'] = line[6]
        kwargs['address']  = ip_address(line[7])  # noqa: E221
        kwargs['port']     = int(line[8])         # noqa: E221
        metadata = line[9].strip('"')
        if metadata:
            metadata = metadata.split('" "')
            metadata = [x.split('=', maxsplit=1) for x in metadata]
            metadata = dict(metadata)
        else:
            metadata = {}
        kwargs['metadata'] = metadata

    update = Update(action, iface, service, name, domain, **kwargs)

    return update


@EntityProxy
class MDNS(Entity):
    @remote_call
    @error(FileNotFoundError, '"avahi-publish-service" is not present or working on this system, ensure avahi-utils is installed')
    async def publish(self, metadata={}):
        cluster_name, port = self.instance
        # Tag all announcements with a unique ID for dedupe
        # needed if listening on multiple interfaces or
        # IPv4 and IPv6. This can be done by avahi but
        # requires setup
        node_id = uuid.uuid4()
        metadata['id'] = node_id
        metadata['cluster_name'] = cluster_name

        txt = [f'{k}={v}' for k, v in metadata.items()]
        port = str(port)
        cmd = publish_cmd + [port] + txt

        async with cmd_wrapper(cmd) as mdns:
            async for line in mdns.stdout:
                print(line)
                pass

    # TODO; remote_stream was removed, work out replacement
    @error(FileNotFoundError, '"avahi-browser" is not present or working on this system, ensure avahi-utils is installed')
    async def browse(self):
        async with cmd_wrapper(discover_cmd) as mdns:
            async for line in mdns.stdout:
                yield parse(line)
