#!/usr/bin/env python

from epicman.server.utils import set_process_affinity

import pytest
import os

NOOP_FUNC = lambda *a, **b: None

@pytest.fixture
def bad_affinity(monkeypatch):
    def fail(*args):
        raise OSError(22, "Invalid Argument")
    monkeypatch.setattr(os, 'sched_setaffinity', fail)
    yield set_process_affinity

@pytest.fixture
def affinity(monkeypatch):
    monkeypatch.setattr(os, 'sched_setaffinity', NOOP_FUNC)
    yield set_process_affinity


def test_empty_list(affinity):
    with pytest.raises(ValueError):
        affinity(",,,")

def test_bad_cpu(bad_affinity):
    with pytest.raises(ValueError):
        bad_affinity('4444')

def test_bad_range(affinity):
    with pytest.raises(ValueError):
        affinity("-")
    with pytest.raises(ValueError):
        affinity("3-")
    with pytest.raises(ValueError):
        affinity("-3")

@pytest.mark.parametrize('mask,cpus', [
    pytest.param('2',       [2],         id='single cpu'),
    pytest.param('2,3,4,5', [2,3,4,5],   id='multiple cpus'),
    pytest.param('2-5',     [2,3,4,5],   id='single range'),
    pytest.param('2-3,5-7', [2,3,5,6,7], id='multiple ranges'),
    pytest.param('2,3,5-7', [2,3,5,6,7], id='mixed values'),
    ])
def test_good_cpu_values(affinity, mask, cpus):
    assert affinity(mask) == cpus

