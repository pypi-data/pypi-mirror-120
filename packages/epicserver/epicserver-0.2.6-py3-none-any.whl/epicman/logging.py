#!/usr/bin/env python3

from traceback import format_exception
from enum import IntEnum, auto
from io import TextIOBase
from time import time as now

import warnings
import blessed
import sys

from . import running_thread

UNKNOWN_ERROR = 100


class Level(IntEnum):
    EXCEPTION = 0
    ERROR = auto()
    WARN = auto()
    INFO = auto()
    DEBUG = auto()


class _log():
    def __init__(self,
                 output: TextIOBase = sys.stderr,
                 level: Level = Level.EXCEPTION
                 ):
        self.stream = output
        self.log_level = level

    def debug(self, _msg: str, *args, **kwargs):
        """Messages to assit in writing code, enabled by pythons debug mode"""
        if __debug__:
            self(Level.DEBUG, _msg, *args, **kwargs)

    def info(self, _msg: str, *args, **kwargs):
        """General information for diagnosing issues via logs after the fact"""
        self(Level.INFO, _msg, *args, **kwargs)

    def warn(self, _msg: str, *args, **kwargs):
        """Non fatal error or informational message about deprication"""
        self(Level.WARN, _msg, *args, **kwargs)

    def error(self, _msg: str, *args, **kwargs):
        "Errors that would crash an individual client/connection or instance"
        self(Level.ERROR, _msg, *args, **kwargs)

    def _horizon(self):
        self(Level.INFO, "Living in the database")

    def exception(self,
                  _msg: str,
                  exit_code: int = UNKNOWN_ERROR,
                  *args,
                  **kwargs,
                  ):
        """A problem that will lead to process exit"""
        self(Level.EXCEPTION, _msg, *args, **kwargs)
        sys.exit(exit_code)

    def __call__(self, level: Level, _msg: str, *args, _err=None, **kwargs):
        if level <= self.log_level:
            if any((args, kwargs)):
               _msg = _msg.format(*args, **kwargs)
            thread = running_thread.get()
            if isinstance(thread, str):
                thread = thread.strip('[]')
                addr, func_name, thread_id = thread.split('][')
            else:
                addr = str(thread.addr)
                func_name = thread.state.__name__
                thread_id = str(thread.id)
            print(f'{term.bold}{now():10.06F}{term.normal} [{term.green(addr)}][{term.yellow(func_name)}][{term.bold_yellow(thread_id)}] {_msg}', file=self.stream)
            if _err:
                traceback = format_exception(*_err)
                for line in traceback:
                    # format_exception may return lines with multiple newlines
                    # inside it
                    line = line.replace('\n ', '\n| ')
                    # Escape dicts that may look like a f-string but are not
                    line = line.replace('{', '{{')
                    line = line.replace('}', '}}')
                    # the lines have newlines embedded so we suppress them
                    # this is slow as we go line by line but if there is
                    # output buffering it will not flush till the print()
                    # post loop
                    print("|", line, end="", file=self.stream)
                print(file=self.stream)


def showwarning(message, category, filename, lineno, file=None, line=None):
    log.warn(f"{filename}:{lineno} {message}")
warnings.showwarning = showwarning

log = _log()
term = blessed.Terminal(stream=log.stream)
