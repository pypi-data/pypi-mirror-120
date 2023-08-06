#!/usr/bin/env python3

from ...logging import log
from ..syscalls import *

from subprocess import Popen, DEVNULL, PIPE
from contextlib import asynccontextmanager
from tempfile import TemporaryDirectory
from os import getpid, sysconf
from functools import wraps


PAGE_SIZE = sysconf('SC_PAGESIZE')
ENCODING='ascii'


@asynccontextmanager
async def cmd_wrapper(cmdline):
    pid = getpid()
    with TemporaryDirectory(prefix='epicman-', suffix=f'.{pid}') as tmpdir:
        cmd = Popen(cmdline, stdin=DEVNULL, stdout=PIPE, stderr=PIPE, cwd=tmpdir, text=ENCODING)
        cmd.stdout = PipeReadEnd(cmd.stdout)
        cmd.stderr = PipeReadEnd(cmd.stderr)
        try:
            yield cmd
        finally:
            # accumulate all error lines in one chunk
            lines = []
            async for line in cmd.stderr:
                lines.append(line)

            # print all log lines back to back to present them together
            cmd.poll() # ensure the ret code is updated
            log.error('"{cmdline}" failed with (rc={cmd.returncode})', cmdline=cmdline, cmd=cmd)
            for line in lines:
                log.error("cmd.stderr: {line}", line=line)

            cmd.terminate()
            await TASK_SLEEP(0.2)
            cmd.kill()


# With a new pipe, if nothing is connected or has not written data
# select() -> read() always, regardless of if here is data to be
# read of not
class PipeReadEnd():
    def __init__(self, pipe, newline='\n'):
        set_nonblocking(pipe)
        self._pipe = pipe
        self.buffer = ''
        self._newline = newline

    async def read(self, size, timeout=0):
        if len(self.buffer) <= size:
            data = self.buffer[:size]
            self.buffer = self.buffer[size:]
            return data
            
        data = await FILE_READ(self._pipe, size - len(buffer), timeout=timeout)

        buffer = self.buffer
        self.buffer = b''
        return buffer + data

    async def __aiter__(self):
        while True:
            data = await FILE_READ(self._pipe, PAGE_SIZE)
            if not data:
                break
            self.buffer += data
            while self._newline in self.buffer:
                line, _, self.buffer = self.buffer.partition('\n')
                yield line
            

def set_nonblocking(file):
    from os import O_NONBLOCK
    from fcntl import fcntl, F_GETFL, F_SETFL
    flags = fcntl(file, F_GETFL)
    flags |= O_NONBLOCK
    fcntl(file, F_SETFL, flags)

