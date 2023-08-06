#!/usr/bin/env python3
"""Creates a Berkley DB to percist objects to disk between restarts"""

from collections.abc import MutableMapping
from .utils import make_key
import dbm

CREATE_DB_IF_NEEDED = 'c'
FILE_PERMS = 0o640


class DBM(MutableMapping):
    def __init__(self, path):
        self.db = dbm.open(path, CREATE_DB_IF_NEEDED, FILE_PERMS)

    def get(self, key, default=None):
        try:
            val = self[key]
        except KeyError:
            val = default
        return val

    def __getitem__(self, key):
        key = make_key(key)
        key = key.encode('utf-8')
        return self.db[key]

    def __setitem__(self, key, value):
        key = make_key(key)
        key = key.encode('utf-8')
        self.db[key] = value

    def __delitem__(self, key):
        key = make_key(key)
        key = key.encode('utf-8')
        del self.db[key]

    def pop(self, key, *args):
        if args:
            value = self.get(key, args[0])
        else:
            value = self[key]
        del self[key]
        return value

    def __len__(self):
        return len(self.db)

    def keys(self):
        return self.db.keys()

    def items(self):
        for key in self.keys():
            yield (key, self[key])

    def values(self):
        for key in self.keys():
            yield self[key]

    def __iter__(self):
        for key in self.keys():
            yield key

    def __contains__(self, key):
        key = f"{key[0]}:{key[1]}".encode('utf-8')
        return key in self.db

    def __enter__(self):
        return self

    def __exit__(self, *err):
        self.close()

    def close(self):
        self.db.close()


def create_db(url):
    _, path = url.split("://", maxsplit=1)
    if not path:
        raise ValueError('No path specified')
    db = DBM(path)
    return db
