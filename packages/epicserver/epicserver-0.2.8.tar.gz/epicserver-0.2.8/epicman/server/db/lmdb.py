#!/usr/bin/env python3
"""Percists game entities to disk using lightning DB"""

from collections.abc import MutableMapping
from .utils import make_key

# 1TB should only consume address space and not memory
MAX_DB_SIZE = 10_000_000_000
CREATE_MODE = 0o750  # exec needed as its creates dirs


try:
    import lmdb
except ImportError:
    import sys
    print("lmdb library not present, try pip installing it or reinstalling this package as epicman[lmdb]", file=sys.stderr)
    raise


class LMDB(MutableMapping):
    def __init__(self, path):
        db = lmdb.Environment(path, map_size=MAX_DB_SIZE, mode=CREATE_MODE)
        self.db = db

    def get(self, key, default=None):
        with self.db.begin() as txn:
            value = txn.get(key)
        return value or default

    def __getitem__(self, key):
        key = make_key(key)
        key = key.encode('utf-8')

        with self.db.begin() as txn:
            value = txn.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        key = make_key(key)
        key = key.encode('utf-8')

        with self.db.begin(write=True) as txn:
            txn.put(key, value)

    def __delitem__(self, key):
        key = make_key(key)
        key = key.encode('utf-8')

        with self.db.begin(write=True) as txn:
            deleted = txn.delete(key)
        if not deleted:
            raise KeyError(key)

    def pop(self, key, default=None):
        with self.db.begin(write=True) as txn:
            value = txn.pop(key)
        if value is None and default is None:
            raise KeyError(key)
        return value or default

    def __len__(self):
        with self.db.begin(write=True) as txn:
            return txn.stat()['entries']

    def __iter__(self):
        with self.db.begin() as txn:
            cur = txn.cursor()
            yield from cur.iternext(keys=True, values=False)

    def keys(self):
        yield from self

    def items(self):
        with self.db.begin() as txn:
            cur = txn.cursor()
            yield from cur.iternext(keys=True, values=True)

    def values(self):
        with self.db.begin() as txn:
            cur = txn.cursor()
            yield from cur.iternext(keys=True, values=True)

    def __contains__(self, key):
        return self[key] is not None

    def __enter__(self):
        return self

    def __exit__(self, *err):
        self.close()

    def close(self):
        self.db.close()


def create_db(url):
    *_, path = url.split("://", maxsplit=1)
    if not path:
        raise ValueError("path to db cannot be blank")
    db = LMDB(path)
    return db
