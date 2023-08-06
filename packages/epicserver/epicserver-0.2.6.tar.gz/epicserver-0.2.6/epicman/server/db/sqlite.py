#!/usr/bin/env python3
"""Percists game entities to disk using sqlite"""

from collections.abc import MutableMapping
import sqlite3


class Sqlite(MutableMapping):
    def __init__(self, url):
        # file:/path/to/fiel;
        db = sqlite3.connect(url, uri=False)
        self.db = db
        db.execute("""CREATE TABLE Entities (
                        namespace text,
                        instance text,
                        data text,
                        PRIMARY KEY(namespace, instance)
                        );""")
        db.execute("""CREATE INDEX Entities_addr ON Entities(instance);""")

    def get(self, key, default=None):
        try:
            val = self[key]
        except KeyError:
            val = default
        return val

    def __getitem__(self, key):
        FIRST_RESULT = FIRST_COLUMN = 0
        namespace, instance = key
        cur = self.db.execute("SELECT data FROM Entities WHERE namespace = ? AND instance = ?;", (namespace, instance))
        vals = cur.fetchall()
        if len(vals) != 1:
            raise KeyError(key)
        return vals[FIRST_RESULT][FIRST_COLUMN]

    def __setitem__(self, key, value):
        namespace, instance = key
        self.db.execute("""INSERT INTO Entities(namespace, instance, data) VALUES (?, ?, ?)
                           ON CONFLICT(namespace, instance) DO UPDATE SET data = excluded.data;""", (namespace, instance, value))

    def __delitem__(self, key):
        namespace, instance = key
        cur = self.db.execute("DELETE FROM Entities WHERE namespace = ? AND instance = ?;", (namespace, instance))
        if cur.rowcount < 1:
            raise KeyError(key)

    def pop(self, key, *args):
        if args:
            value = self.get(key, args[0])
        else:
            value = self[key]
        del self[key]
        return value

    def __len__(self):
        return self.db.execute("SELECT count(*) FROM Entities;")[0]

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.db == other.db

    def __iter__(self):
        pass

    def keys(self):
        pass

    def items(self):
        pass

    def values(self):
        pass

    def __contains__(self, key):
        try:
            self[key]
            val = True
        except KeyError:
            val = False
        return val

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
    return Sqlite(path)
