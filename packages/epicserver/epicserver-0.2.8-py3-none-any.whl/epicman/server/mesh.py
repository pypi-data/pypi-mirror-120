#!/usr/bin/env python

from ..game.socket import AsyncSocket
from ..logging import log
from .syscalls import *

from collections import UserList
from typing import List, Tuple
from functools import wraps
import resource
import socket
import sys

#from hashlib import blake2b as hash_algo
#try:
#    hash_algo(usedforsecurity=False)
#except TypeError:
#    hash_algo()

# monitoring
# routing
# gosip

PAGE_SIZE = resource.getpagesize()

SPEED_1_MEGABIT = 1_000_000
SPEED_10_MEGABIT = SPEED_1_MEGABIT * 10
SPEED_40_MEGABIT = SPEED_1_MEGABIT * 40
SPEED_100_MEGABIT = SPEED_10_MEGABIT * 10
SPEED_GIGABIT = SPEED_100_MEGABIT * 10
SPEED_10_GIGABIT = SPEED_GIGABIT * 10


class S2S():
    def __init__(self, addr: Tuple[str, int], hints: list=[]):
        self.listen_addr = addr
        self.hints = hints or []
        self.known = []

    async def incomming(self):
        log.info(f"Connection from server on S2S port: {c_addr}")
        data = await client.recv(512)
        while data:
            data = await client.recv(512)
            log.info(f'XXX len={len(data)} {data.hex()}')
        client.close()

    async def s2s_listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        sock.bind(self.listen_addr)
        sock.listen()
        sock = AsyncSocket(sock)
        while True:
            conn = await sock.accept()
            addr = conn[1]
            addr = "{}:{}".format(*addr)
            await TASK_SEND(self.incomming, conn)

    async def outgoing(self):
        addr = await TASK_RECV()
        # we dont set a timeout as on localhost we know straight away
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(addr)
            log.info('connected')
            sock = AsyncSocket(sock)
            await sock.send(b'Hello')
            log.info('sent hello')
        finally:
            sock.close()
        log.info('closed')
    async def bootstrap_s2s(self):
        for hint in self.hints:
            await TASK_SEND((self.outgoing, f'{hint[0]}:{hint[1]}'), hint)

def start_bootstrap():
    pass
def start_s2s():
    pass

async def start_app():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(False)
    # These options are tunned for LAN/Datacenter level latencies
    # taking more than one second for rtt is highly unlikley 
    # with 1-2mS expected
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    s.setsockopt(socket.SOL_TCP,    socket.TCP_NODELAY, True)
    ###### NON PORTABLE OPTIONS ######
#    s.setsockopt(socket.SOL_SOCKET, socket.SO_BUSY_POLL, 100) #uS
    s.setsockopt(socket.SOL_TCP,    socket.TCP_DEFER_ACCEPT, 3)
    # connection level service monitoring
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
    s.setsockopt(socket.SOL_TCP,    socket.TCP_KEEPIDLE, 1)
    s.setsockopt(socket.SOL_TCP,    socket.TCP_KEEPINTVL, 1)
    # We use 500mS here as it allows for some congestion on the remote end
    # though it does not include processing time as this is ourside of
    # the scope of this TCP level monitor
    s.setsockopt(socket.SOL_TCP,    socket.TCP_USER_TIMEOUT, 500) #mS
#    s.setsockopt(socket.SOL_IP,     socket.IP_RECVERR, True) #mS
    addr = ('127.0.0.1', 30303)
    s.bind(addr)
    s.listen()
    s = AsyncSocket(s)

    log.info(f'listening on {addr}')
    await TASK_SEND((accept_conn, "{}:{}".format(*addr)), s)

    bootstrap_addresses = [
        ("127.0.0.1", 8081),
        ("127.0.0.1", 8082),
        ("127.0.0.1", 8083),
        ]
    gossip = Gossip(bootstrap_addresses)
    monitoring = Monitoring(Gossip)

    # Gossip discovers hosts
    await gossip.start()
    # Monitor subscribes to Gossip and confirms they are alive
    await monitoring.start()
    # Alive hosts are added to routing
    await Routing(monitoring).start()
    # the above may leave gaps however we should only be sending messages
    # to things we are monitoring, we COULD open a connection and use that
    # as an implicit monitor


def calc_buffer_size(sock: socket.socket, link_speed: int=SPEED_GIGABIT):
    # tcpi_rcv_rtt - how long in uS that the remote client would exaust the current window
    TCP_INFO_LEN = 0 # needs C level support or ctypes?
    #retrive rtt time from TCP_INFO
    tcp_info = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_INFO, TCP_INFO_LEN) 
    round_trip_time = tcp_info.tcpi_rtt
    buffer_size = link_speed * round_trip_tim
    
    # Convert to bytese
    buffer_size /= 8
    # truncate lower bit to be a multiple of PAGE_SIZE
    buffer_size /= PAGE_SIZE
    # Add one additional PAGE_SIZE for saftey
    buffer_size += 1
    buffer_size *= PAGE_SIZE

    return buffer_size

class Routing():
    monitored: list # Monitored nodes we are always conencted to
    conntaced: list # Nodes we have connected to but are not part of montioring policy
    known: list # all known nodes picked up from gossip
    def __init__(self, ):
        self.table = RoutingTable
    
    async def connect(object_addr):
        node = self.ring[object_addr]
        if node in self.monitored:
            return self.monitored[addr]
        elif node in self.connected:
            return self.connected[addr]
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(False)
            s = await connect(addr)
            # set socket options here
            # * hearbeat for regualr RTT times
            return s

    async def recv_msg(self, socket):
        addr = socket.getpeername()
        while True:
            # Packet recv
            msg_length = await SOCK_RECV(2)
            if len(msg_length) != 2:
                break
            buffer = b''
            while len(buffer) < msg_length:
                data = await SOCK_RECV(msg_length)
                if not data:
                    break
                buffer += data
            packet = depacket(buffer)

            # Packet processing
            if isinstance(packet, Gossip):
                # update local rt
                # ensure we dont reinject this into running app
                continue
            elif isinstance(packet, CloseConnection):
                log.warn("Disconnect from {addr}")
                if addr in self.monitored:
                    # remove
                    pass
                elif addr in self.connected:
                    # remove
                    pass
                else:
                    # connection of opertunity, not tracked
                    pass
                return
                

            await SOCK_SEND(packet.dst, packet.body)
            
        log.warn("Bad disconnect from {addr}")
        
    async def send_msg(self, task, msg):
        pass


class RoutingTable(UserList):
    def __getitem__(self, key):
        # this data structure loops around and is
        # shaped like a circle so only lookup failure
        # is when nothing added
        if not self.data:
            raise KeyError(key)
            
        last = self.data[-1]
        for cur in self.data:
            if cur[0] > key:
                break
            last = cur
        return last[1]
        
    def __setitem__(self, key, val):
        self.data.append((key, val))
        self.data.sort()
        
    def __delitem__(self, key):
        for i in range(len(self.data)):
            if self.data[i][0] == key:
                del self.data[0]
                break
        else:
            raise KeyError(key)


