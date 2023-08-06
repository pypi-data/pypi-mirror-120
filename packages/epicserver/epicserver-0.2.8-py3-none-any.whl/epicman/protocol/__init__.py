#!/usr/bin/env python3

from typing import NamedTuple
from struct import Struct
from enum import IntEnum, auto

from .. import common

PORTABLE_ALIGNMENT = "<"
ENTITY = 'H'
PLAYER_ENTITY = 0
DIRECTION = "B"

class Direction(IntEnum):
    UP = 0
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

 
# Ordered message ID types
ClientEntityUpdate = Struct(PORTABLE_ALIGNMENT + ENTITY + DIRECTION)
ServerEntityUpdate = Struct(PORTABLE_ALIGNMENT + ENTITY + DIRECTION)


class Messages():
    def __init__(self, sock):
        self.sock = sock

    def recv_queue(self):
        msgs = []
        updates = self.sock.recv(common.CLIENT_PACKET_SIZE)
        next_packet = 0
        while next_packet < len(updates):
            msg_type = updates[next_packet]
            next_packet += 1
            msg_len = updates[next_packet]
            next_packet += 1
            msg = updates[next_packet:next_packet + msg_len]
            next_packet += msg_len
            msgs.append((msg_type, msg))

        return msgs

    def recv():
        msg_type, msg_len = self.sock.recv(2)
        msg = self.sock.recv(msg_len)
        return msg_type, msg

    def send_queue(self, updates):
        MSG_CLIENT_UPDATE = 1
        buffer = bytearray(common.CLIENT_PACKET_SIZE)
        next_packet = 0
        for msg_type, msg in updates:
            buffer[next_packet] = msg_type
            next_packet += 1
            buffer[next_packet] = len(msg)
            next_packet += 1
            buffer[next_packet:next_packet + len(msg)] = msg
            next_packet += len(msg)
        self.sock.send(buffer[:next_packet])

    def send(self, update):
        return self.send_queue([update])

    def __iter__(self):
        while True:
            yield from self.recv_queue()
