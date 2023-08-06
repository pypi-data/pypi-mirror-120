#!/usr/bin/env python3
"A dummy in memeory backend that just stores everythign in an in a dictonary"

from .utils import make_key


class ClosableDict(dict):
    def close(self):
        """dummy close method as we do not persist"""
        pass

    def __enter__(self):
        return self

    def __exit__(self, *tb):
        self.clear()

    def __getitem__(self, key):
        k = make_key(key)
        return super().__getitem__(k)

    def __setitem__(self, key, value):
        k = make_key(key)
        return super().__setitem__(k, value)

    def __delitem__(self, key):
        k = make_key(key)
        super().__delitem__(k)

    def pop(self, key):
        k = make_key(key)
        return super().pop(k)


def create_db(url):
    return ClosableDict()
