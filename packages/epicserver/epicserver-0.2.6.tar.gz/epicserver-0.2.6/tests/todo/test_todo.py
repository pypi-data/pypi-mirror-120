#!/usr/bin/env python3

import pytest

from warnings import warn_explicit
from subprocess import getoutput
from collections import namedtuple
from pathlib import Path
import re

find_todo = re.compile(r'#\s*[tT][oO][dD][oO]\s*:?\s(.*)').search
find_bug = re.compile(r'#\s*[bB][uU][gG]\s*:?\s(.*)').search

BASE_PATH = Path(getoutput('hg root'))

comment_info = namedtuple('comment_info', 'file line txt')

def scan_file(path, match):
    with path.open() as f:
        for i, line in enumerate(f, 1):
            m = match(line)
            if m:
                comment = m.groups()[0]
                yield comment_info(path, i, comment)

def scan_dir(dir, match):
    for path in Path(dir).rglob('*.py'):
        if path.is_symlink():
            continue
        yield from scan_file(path, match)
    
found_todo = list(scan_dir(BASE_PATH/'epicman', find_todo))
found_bug = list(scan_dir(BASE_PATH/'epicman', find_bug))

@pytest.mark.parametrize('todo', found_todo)
@pytest.mark.todo
def test_todo(todo):
    file = todo.file.relative_to(BASE_PATH)
    line = todo.line
    warn_explicit(f'{file} {line}: {todo.txt}', FutureWarning, str(file), line)

@pytest.mark.parametrize('bug', found_bug)
@pytest.mark.bug
def test_bug(bug):
    file = bug.file.relative_to(BASE_PATH)
    line = bug.line
    pytest.fail(f'{file} {line}: {bug.txt}')
