#!/usr/bin/env python

from epicman.middleware.mesh import RoutingTable

import pytest
import random

@pytest.fixture
def rt():
    return RoutingTable()

NO_KEY = 0
TEST_KEY = 50

def test_rt_empty_lookup(rt):
    with pytest.raises(KeyError):
        rt[NO_KEY]
        
def test_rt_single_lookup(rt):
    # Table
    rt[TEST_KEY * 1] = False
    rt[TEST_KEY * 2] = True
    # this is the point in the table we are looking up and
    # should go to the previous __setitem__()
    rt[TEST_KEY * 3] = False
    
    assert rt[TEST_KEY * 2], 'Wrong value returned by routing table lookup'

def test_rt_multi_lookup(rt):
    ROUNDS = ENTRIES = 10
    
    for i in range(ENTRIES):
        rt[TEST_KEY * i] = i

    # We randomise the lookups to avoid any potential issues with ordering
    # this is more caution than strictly required
    checks = list(range(ROUNDS))
    random.shuffle(checks)
    for i in checks:
        assert rt[(TEST_KEY * i) + 1] == i, 'Wrong value returned by routing table lookup'

def test_rt_add(rt):
    rt[TEST_KEY] = 'valid'

def test_rt_add_multi(rt):
    rt[TEST_KEY * 1] = 'valid'
    rt[TEST_KEY * 2] = 'valid'
    rt[TEST_KEY * 3] = 'valid'

    assert len(rt) == 3, 'Incorrect number of entries in the routing table'

def test_rt_del(rt):
    rt[TEST_KEY] = 'valid'
    del rt[TEST_KEY]
    
def test_rt_del_empty(rt):
    with pytest.raises(KeyError):
        del rt[NO_KEY]

def test_rt_set(rt):
    rt[TEST_KEY] = 'valid'

def test_rt_set_update(rt):
    ROUNDS = 3
    for i in range(ROUNDS):
        rt[TEST_KEY] = i
        assert rt[TEST_KEY] == i

    assert len(rt) == ROUNDS, 'did not find extra entries in the routing table from early iterations'



def test_rt_returns_correct_range(rt):
    rt[1000] = 1000
    rt[2000] = 2000
    rt[3000] = 3000

    assert rt[0] == 3000, 'Routing Table does not wrap around'
    assert rt[3500] == 3000, 'Routing Table does not wrap around'
    assert rt[1000] == 1000, 'Routing Table does not return correct val on exact match'
    assert rt[1500] == 1000, 'Routing Table does not return correct val in middle of slice'


def test_rt_is_iterable(rt):
    keys = [1,2,3,4,5]
    for key in keys:
        rt[key] = key

    for entry, expected in zip(rt, keys):
        assert entry == (expected, expected)


def test_repr(rt):
    repr(rt)
    rt[2] = 3
    repr(rt)


def test_len(rt):
    assert len(rt) == 0
    for i in range(1, 5):
        rt[i] = i
        assert len(rt) == i
