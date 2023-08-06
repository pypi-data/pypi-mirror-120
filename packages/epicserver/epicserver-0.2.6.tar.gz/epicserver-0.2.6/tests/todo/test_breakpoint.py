#!/usr/bin/env python3

import pytest

from warnings import warn_explicit
from subprocess import getoutput
from collections import namedtuple
from pathlib import Path
import re

contains_breakpoint = re.compile(r'breakpoint\(\)').search

BASE_PATH = Path(getoutput('hg root'))

comment_info = namedtuple('comment_info', 'file line txt')

def scan_file(path, match):
    with path.open() as f:
        for i, line in enumerate(f, 1):
            m = match(line)
            if m:
                start, _ = m.span()
                # commented out
                if '#' in line[:start]:
                    break
                if '# noqa' in line:
                    break
                yield comment_info(path, i, line)

def scan_dir(dir, match):
    for path in Path(dir).rglob('*.py'):
        if path.is_symlink():
            continue
        yield from scan_file(path, match)
    
found_breakpoint = list(scan_dir(BASE_PATH/'epicman', contains_breakpoint))

@pytest.mark.parametrize('breakpoint', found_breakpoint)
def test_breakpoint(breakpoint):
    file = breakpoint.file.relative_to(BASE_PATH)
    line = breakpoint.line
    pytest.fail(f'{file} {line}: {breakpoint.txt}')
