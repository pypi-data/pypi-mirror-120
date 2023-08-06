#!/usr/bin/env python3

from contextlib import contextmanager
from typing import Dict

from ..server.syscalls import *
from ..logging import log

import socket
import os


@contextmanager
def cleanup_socket(addr):
    try:
        yield
    finally:
        os.unlink(addr)

def server(s: socket.socket):
    clients: Dict[int, socket.socket] = {}
    import select
    try:
        while True:
            rd, wr, err = select.select([s] + list(clients.keys()), [], [])
            for fileno in rd:
                if fileno == s.fileno():
                    c, addr = s.accept()
                    c_handler = client(c)
                    clients[c] = c_handler
                    c_handler.send(None) # prime the task
                else:
                    c_handler = clients[fileno]
                    data = fileno.recv(PACKET_SIZE)
                    cmd = c_handler.send(data) # we ignore cmd here as we only have one
                    queue.append(cmd.msg)
                    # todo: implement ticks
                    # todo: implement broadcasting
                    # todo: client hang up
    finally:
        for client in clients:
            # todo: notify clients with timeouts
            addr = "Unknown"
            log.info("Shutting down client {client}@{addr}", client=client, addr=addr)
            client.close()

class SocketEdge():
    def __init__(self, sock):
        self.clients = {}
        self.socket = sock

    async def packetize(self, socket):
        LENGTH_BYTES = 2
        MAX_PACKET_LENGTH = 500
        msg_length = await READ_SOCKET(socket, LENGTH_BYTES)
        msg_length = int.from_bytes(msg_length, 'little', signed=False)
        if msg_length > MAX_PACKET_LENGTH:
            raise ValueError("Remote end attempted to send a packet larger than maximum allowed")
        
        msg = await READ_SOCKET(socket, msg_length)

        return msg
        
    async def log_in_client(self, socket):
        # read handshake
        msg = await packetize(socket)
        # send version
        PROTOCOL_VERSION = b'ALPHA'
        await WRITE_SOCKET(socket, PROTOCOL_VERSION)
        remote_version = await packetize(socket)
        if remote_version != PROTOCOL_VERSION:
            raise VersionMismatch(f'Client sent version {remote_version} but we only support {PROTOCOL_VERSION}')

        # read username
        client_name = await packetize(socket)

        return client_name

    async def client_router(self, socket):
        # perform authenticaion handshake
        # send 'init' message to logged in client clusterproc
        # read packets from socket
        # route to logged in client
        with socket: # ensure we dont leak client sockets
            client_addr = await log_in_client(socket)
            while True:
                msg = await packetize(socket)
                await TASK_SEND(client_addr, msg)

    async def server_loop(self):
        sock = self.socket
        while True:
            await sock.accept()
            client_sock, addr = await SOCKET_READ(sock)
            name = f"{addr[0]}:{addr[1]}"
            # packetization? where does that come from here?
            client = await SPAWN_TASK(name, self.client_connection, client_sock)

    # what happens if a client exits?
    async def client_loop(self):
        while True:
            try:
                msgs = await TASK_WAIT()
            except ServerUpdate as update:
                await TASK_SEND(update.msg)
