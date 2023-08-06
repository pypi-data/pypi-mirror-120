#!/usr/bin/env python3

import subprocess
# While we dont use this module we import it 
# to ensure epicman is avlaible in our PYTHONPATH
import epicman
import pytest
import sys

EPICMAN = [sys.executable, '-m', 'epicman.server']

DEVNULL = subprocess.DEVNULL

def test_cli_no_args():
    """Ensure help appears on bad input"""
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_output(EPICMAN, stderr=DEVNULL)

def test_cli_dummy_app():
    APP = ['epicman.helpers:dummy_app']
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_output(EPICMAN + APP, stderr=DEVNULL)

def test_cli_help():
    """Ensure help output works without issue"""
    output = subprocess.check_output(EPICMAN + ['-h'], stderr=DEVNULL)
    assert b'--version' in output
    assert b'--help' in output
    assert b'entrypoint' in output

@pytest.mark.parametrize('setting',
    [['-n', 'test cluster'],
     ['-m'],
     ['-b', '127.0.0.1:1'],
    ])
def test_cluster_bad_settings(setting):
    with pytest.raises(subprocess.CalledProcessError):
        output = subprocess.check_output(EPICMAN + setting, stderr=DEVNULL)
        # confirm we explain what needs to be dont to correct error
        assert b"--listen" in output
