#!/usr/bin/env python3

from importlib import import_module
from typing import List, Callable

from argparse import ArgumentTypeError
from ipaddress import ip_address, IPv4Address, IPv6Address
from functools import wraps

import socket
import re
import os


def get_entrypoint(entrypoint: str) -> Callable:
    if entrypoint.count(":") == 0:
        raise ValueError('No function name found in entrypoint, needs a ":"')
    elif entrypoint.count(":") > 1:
        raise ValueError('Entrypoint is invalid, contains too many ":"')

    module_name, func_name = entrypoint.split(":", maxsplit=1)

    # can raise Module* issues
    module = import_module(module_name)
    func = getattr(module, func_name, None)
    if not callable(func):
        raise ValueError("Entrypoint does not point to a callable function")

    return func


def set_process_affinity(cpus: str) -> List[int]:
    map = cpus.split(',')
    cpu_map = []
    try:
        for cpu in map:
            if '-' in cpu:
                a, b = cpu.split('-', maxsplit=1)
                start = int(a)
                # this is just how range works, b is not inclusive
                # so we add 1 to ensure it is included in the output
                end = int(b) + 1
                cpu_map.extend(list(range(start, end)))
            else:
                cpu_map.append(int(cpu))

        CURRENT_PROC = 0
        os.sched_setaffinity(CURRENT_PROC, cpu_map)
    except (ValueError, OSError) as err:
        raise ValueError("CPU list is invalid") from err

    return cpu_map


# must contain at least one letter to be a domain name
# this is simple and naive and intended to filter out
# obviously bad domain names (such as those with spaces)
# before we do a more robust check at connect()
is_hostname = re.compile(r'[a-zA-Z0-9_\-\.]*[:alnum:][a-zA-Z0-9_\-\.]*').fullmatch


def single_address(s):
    try:
        addr, port = s.rsplit(":", maxsplit=1)
    except ValueError:
        raise ArgumentTypeError(f'Provided address does not contain a port: "{s}"')

    # see below for ipv6 handling, if a port is omitted (and its just an ipv6
    # address) then split will incorrectly take part of the ipv6 address as a
    # port. while later code will pick this up it is easier to provide a more
    # robust explanation of the failure that is more indicative of the issue
    # to the user
    if ']' in port:
        raise ArgumentTypeError(f'Provided address does not contain a port: "{s}"')

    # Best effort attempt to convert service name to a port
    # failures will be picked up by int() conversion below
    try:
        port = socket.getservbyname(port)
    except (ValueError, OSError):
        pass

    try:
        port = int(port)
    except ValueError:
        raise ArgumentTypeError(f'Port number is not a valid port name or number: "{port}"')
    if not (0 < port < 65536):
        raise ArgumentTypeError(f'Port number is invalid and should be between 0 and 65536: "{port}"')

    # ipv6 addresses may need to be wrapped in '[]' to avoid ambiguity between
    # an ipv6 address and ipv6 address with a port number
    addr = addr.strip('[]')

    # the blank form of an ip address ('') should default to all interfaces
    # it is tempting to catch this and make it 0.0.0.0 however this will break
    # mixed ip environments, instead pass it through by special casing the
    # senario where there is a value provided
    try:
        addr = ip_address(addr)
        addr = map_v4_to_v6(addr)
        return (addr, port)
    except ValueError:
        pass

    try:
        addr = addr.encode('idna').decode('ascii')
    except UnicodeError:
        raise ArgumentTypeError(f'Hostname is a IDNA Domain name with invalid characters: "{s}"')
    if is_hostname(addr) is None:
        raise ArgumentTypeError(f'Hostname is not a valid domain name or IP: "{s}"')

    return (addr, port)


def port_or_addr(s):
    if s.startswith(':'):
        s = s[1:]
    if ":" not in s:
        if s.isdecimal():
            port = int(s)
        else:
            try:
                port = socket.getservbyname(s)
            except (ValueError, OSError):
                raise ArgumentTypeError(f'Port is not a known port name: "{s}"')
        if not (0 < port < 65536):
            raise ArgumentTypeError(f'Port number should be between 0 and 65536: "{port}"')
        return ('', port)
    return single_address(s)


def comma_seperated(typ):
    @wraps(comma_seperated)
    def inner(s):
        s = s.split(",")
        s = [x.strip() for x in s]
        s = [typ(x) for x in s]
        return s
    return inner

def map_v4_to_v6(addr):
    if isinstance(addr, IPv4Address):
        addr = IPv6Address('::FFFF:' + str(addr))
    return addr
