#!/usr/bin/env python3

__author__ = "Blitz.Works"
__email__ = "code@blitz.works"
__license__ = "BSD (3 Clause)"
__url__ = "http://blitz.works/epic/epic-server/"

# Ensure this is set up early in module import
# so that the default is set before any potential
# usage, ORDERING is IMPORTANT here
from contextvars import ContextVar
from typing import Tuple, Any
running_thread: ContextVar[Tuple[Tuple["Entity", Any], int]] = ContextVar('running_thread')
# Dont import until running_thread is defined as others
# need this to exist for thier imports chained from
# this to succeed
DEFAULT_THREAD = '[system:0][system][0]'
running_thread.set(DEFAULT_THREAD)
from .objects import Entity # delay import to avoid circlular deps

from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("epicman-server")
except PackageNotFoundError:
    # package is not installed
    pass
