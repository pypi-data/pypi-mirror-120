#!/usr/bin/env python3

from epicman.objects import EntityProxy, Entity, callable_entity, remote_call
from epicman.syscalls import *
from epicman.server import SchedulerError, MainLoop

import pytest

INITAL_VAL = 0

## State to be persisted
#       | CHECKPOINT | Return
# ------+------------+---------
# !Dict |   _save()  | _save()
#  Dict |    Dict    |  Dict

@EntityProxy
class Persist_by_state(Entity):
    _persist = ['val']
    val: int = INITAL_VAL
    @remote_call
    async def __call__(self):
        self.val += 1

@EntityProxy
class Persist_by_syscall(Entity):
    _persist = ['val']
    val: int = INITAL_VAL
    @remote_call
    async def __call__(self):
        self.val = self.val + 1
        await CHECKPOINT()

@callable_entity
async def persist_func_by_syscall(val=INITAL_VAL):
    val += 1
    await CHECKPOINT(state=locals())


def start_proc(dst):
    async def inner():
        await dst()
    return inner


@pytest.mark.parametrize('entity', 
    ['test'@persist_func_by_syscall,
     'test'@Persist_by_state,
     'test'@Persist_by_syscall,
    ])
def test_syscall_checkpoint(entity):
    db = {}
    for round in range(INITAL_VAL + 1, 5):
        with pytest.raises(SchedulerError):
            main_loop = MainLoop(db)
            main_loop.run_forever([start_proc(entity)])
        assert db, f'Round: {round} - Expected an object to be persisted to the DB'
        assert 'val' in db[entity], f'Round: {round} - "val" not present in state from backend db'
        assert db[entity]['val'] == round, f'Round: {round} - backend db val does not match expected value'
