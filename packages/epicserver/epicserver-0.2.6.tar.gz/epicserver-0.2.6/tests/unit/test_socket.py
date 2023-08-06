#!/usr/bin/env python3


from epicman.helpers.socket import AsyncSocket, async_socket
from epicman.syscalls import *

from types import CoroutineType

import pytest
import socket
import random

DATA = random.getrandbits(8*32).to_bytes(32, 'little')
FULL_DATA = len(DATA)
PARTIAL_DATA = len(DATA) // 2
NO_DATA = 0
ERROR = -1

@pytest.fixture
def sock():
    s = async_socket()
    yield s
    s.close()

def async_chat(co, script):
    try:
        for msg, reply, *error_msg in script:
            error_msg.append('')
            error_msg = error_msg[0]
            ret = co.send(msg)
            assert reply(ret), error_msg
        raise ValueError("coroutine exhausted all of chat script without returning")
    except StopIteration as ret:
        return ret.value

def test_accept(sock):
    co = sock.accept()
    assert isinstance(co, CoroutineType), 'accept() call did not return an awaitable'
    ret = async_chat(co, [
        (None, lambda x: isinstance(x, SOCK_ACCEPT)),
        # we reuse the same listening socket as a client connection
        # as we dont do any special checks on it
        ((sock._read_sock, ('127.0.0.1', 3999)), None),
        ])
    assert isinstance(ret[0], AsyncSocket)
    assert len(ret) == 2

def test_full_read(sock):
    co = sock.recv(len(DATA))
    assert isinstance(co, CoroutineType), 'read() call did not return an awaitable'
    ret = async_chat(co, [
        (None, lambda x: isinstance(x, SOCK_RECV)),
        (DATA, None),
        ])
    assert ret == DATA

def test_partial_read(sock):
    co = sock.recv(len(DATA))
    assert isinstance(co, CoroutineType), 'read() call did not return an awaitable'
    ret = async_chat(co, [
        (None, lambda x: isinstance(x, SOCK_RECV)),
        (DATA[:2], None),
        ])
    assert ret == DATA[:2]

def test_no_read(sock, monkeypatch):
    co = sock.recv(len(DATA))
    assert isinstance(co, CoroutineType), 'read() call did not return an awaitable'
    ret = async_chat(co, [
        (None, lambda x: isinstance(x, SOCK_RECV)),
        (b'', None),
        ])
    assert ret == b''

def test_full_write(sock):
    FULL_DATA = len(DATA)
    co = sock.send(DATA)
    assert isinstance(co, CoroutineType), 'write() call did not return an awaitable'
    ret = async_chat(co, [
        (None, lambda x: isinstance(x, SOCK_SEND)),
        (FULL_DATA, None),
        ])
    assert ret == FULL_DATA

def test_partial_write(sock):
    co = sock.send(DATA)
    assert isinstance(co, CoroutineType), 'write() call did not return an awaitable'
    ret = async_chat(co, [
        (None, lambda x: isinstance(x, SOCK_SEND)),
        (PARTIAL_DATA, lambda x: isinstance(x, SOCK_SEND)),
        (NO_DATA, None),
        ])
    assert ret == PARTIAL_DATA

def test_no_write(sock):
    co = sock.send(DATA)
    assert isinstance(co, CoroutineType), 'write() call did not return an awaitable'
    ret = async_chat(co, [
        (None, lambda x: isinstance(x, SOCK_SEND)),
        (NO_DATA, None),
        ])
    assert ret == NO_DATA
