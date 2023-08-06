#!/usr/bin/env python3

from typing import MutableMapping

from importlib.metadata import entry_points


backends = entry_points()['epicman.server.db.backends']


def get_backend(url: str) -> MutableMapping:
    engine, *_ = url.split('://')
    engine = engine or 'default'

    # importlib_meta DOES have select() while .meta does not
    # lets just go with the offical way so we can remove
    # the TODO above
    found_backends = [x for x in backends if x.name == engine]
    if not found_backends:
        raise KeyError(engine)
    backend = found_backends[0]

    try:
        db = backend.load()(url)
    except Exception as err:
        raise ValueError(err) from err

    return db
