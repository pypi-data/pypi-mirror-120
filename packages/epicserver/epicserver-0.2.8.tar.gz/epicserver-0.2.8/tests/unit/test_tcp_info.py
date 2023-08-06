#!/usr/bin/env python

from epicman.helpers.socket import get_tcp_info, TCP_Info

import socket
import pytest
import errno
import os

@pytest.fixture
def tcp_sock():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        yield sock

@pytest.fixture
def udp_sock():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        yield sock

@pytest.fixture
def devnull_file():
    with open(os.devnull, 'r') as file:
        yield file


def test_works_fd(tcp_sock):
    ret = get_tcp_info(tcp_sock.fileno())
    assert isinstance(ret, TCP_Info)

def test_works_socket(tcp_sock):
    ret = get_tcp_info(tcp_sock)
    assert isinstance(ret, TCP_Info)

def test_rejects_non_filelike():
    with pytest.raises(ValueError):
        ret = get_tcp_info(None)

    with pytest.raises(ValueError):
        ret = get_tcp_info('sada')

def test_udp_sock(udp_sock):
    try:
        get_tcp_info(udp_sock.fileno())
    except OSError as err:
        assert err.errno == errno.ENOTSUP
    else:
        pytest.fail('Incorrect error raised')
        
def test_on_disk_file(devnull_file):
    try:
        get_tcp_info(devnull_file.fileno())
    except OSError as err:
        assert err.errno == errno.ENOTSOCK
    else:
        pytest.fail('Incorrect error raised')
