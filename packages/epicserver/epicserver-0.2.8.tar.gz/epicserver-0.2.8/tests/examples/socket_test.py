from epicman.syscalls import *
from epicman.helpers.socket import async_socket
from epicman.logging import log
import socket

MAX_PACKET = 512

async def client():
    sock, addr = await TASK_RECV()
    log.info(f"Client spawned for {addr}")
    data = await sock.recv(MAX_PACKET)
    while data:
        log.info(f'XXXX: Recived data from client: 0x{data.hex()}')
        data = await sock.recv(MAX_PACKET)

async def incomming_listener():
    sock = await TASK_RECV()
    log.info(f'recived socket {sock}')
    while True:
        client_sock, addr = await sock.accept()
        log.info(f"Connection from client: {addr}")
        await TASK_SEND((client, "{}:{}".format(*addr)), (client_sock, addr))

async def game_start():
    sock = async_socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = ('127.0.0.1', 9039)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sock.bind(addr)
    sock.listen()
    log.info(f'listening on {addr}')
    await TASK_SEND((incomming_listener, "{}:{}".format(*addr)), sock)
