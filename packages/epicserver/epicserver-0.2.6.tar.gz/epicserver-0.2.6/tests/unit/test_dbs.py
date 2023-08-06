#!/usr/bin/env pytest

from epicman.server.db.sqlite import create_db as sqlite
from epicman.server.db.dbm import create_db as dbm
from epicman.server.db.dict import create_db as dict

from pytest import raises
import pytest

backends = []
backends.append(('sqlite', sqlite))
backends.append(('dbm', dbm))
backends.append(('dict', dict))
try:
    from epicman.server.db.lmdb import create_db as lmdb
    backends.append(('lmdb', lmdb))
except ModuleNotFoundError:
    pass

@pytest.fixture(params=backends)
def db(request, tmpdir):
    typ, create_db = request.param
    url = f"{typ}://{tmpdir}/test.db"
    db = create_db(url)
    yield db
    db.close()

OBJ_SPACE = "myspace"
TEST_VALUE = b"value"
NO_KEY = OBJ_SPACE, 'no key'
VALID_KEY = OBJ_SPACE, 'valid key'
TEST_KEY_1 = OBJ_SPACE, 'test key 1'
TEST_KEY_2 = OBJ_SPACE, 'test key 2'
TEST_KEY_3 = OBJ_SPACE, 'test key 3'
TEST_KEY_4 = OBJ_SPACE, 'test key 4'
TEST_KEY_5 = OBJ_SPACE, 'test key 5'
VALID_KEYS = [
    TEST_KEY_1,
    TEST_KEY_2,
    TEST_KEY_3,
    VALID_KEY,
    TEST_KEY_4,
    TEST_KEY_5,
    ]

def test_get(db):
    # msg="DB returned data for a key that had not been added"
    with raises(KeyError):
        db[NO_KEY]
    db[VALID_KEY] = TEST_VALUE
    assert db[VALID_KEY] == TEST_VALUE

def test_set(db):
    db[VALID_KEY] = TEST_VALUE
    assert db[VALID_KEY] == TEST_VALUE
    db[VALID_KEY] = TEST_VALUE + TEST_VALUE
    assert db[VALID_KEY] == TEST_VALUE + TEST_VALUE


def test_del(db):
    # msg="DB did not raise a key error for a non-existent key"
    with raises(KeyError):
        del db[NO_KEY]
    db[VALID_KEY] = TEST_VALUE
    del db[VALID_KEY]
    assert VALID_KEY not in db, "Value not deleted from database"
    

def test_pop(db):
    # msg="DB did not raise a key error for a non-existent key"
    with raises(KeyError):
        db.pop(NO_KEY)
    db[VALID_KEY] = TEST_VALUE
    assert db.pop(VALID_KEY) == TEST_VALUE, "Value did not match one inserted into database"
    assert VALID_KEY not in db, "Value not deleted from database"
    

def test_contains(db):
    assert (NO_KEY in db) == False, "DB incorectly asserted it contained an entry that had not been added"
    

def test_has_close(db):
    assert hasattr(db, 'close'), "DB has no close method which is part of the contract"

def test_context_manager(db):
    assert hasattr(db, '__enter__'), "DB is not a context manager which is part of the contract - missing __enter__"
    assert hasattr(db, '__exit__'), "DB is not a context manager which is part of the contract - missing __exit__"

    assert db.__enter__() == db, "db context manager does not return the same db object"
