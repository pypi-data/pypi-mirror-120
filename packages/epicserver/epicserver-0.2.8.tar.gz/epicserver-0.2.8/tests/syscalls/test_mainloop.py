#!/usr/bin/env python3
"""This test suite is about ensuring the application does not crash under
general behavior when an applicaiton returns somthign unexpected. In addition
if covers some explicit cases where we DO expect the app to exit such as
* system.exit()
* assert False
with some of these being used for testing or is the behavior we want
"""

from epicman.server import MainLoop, SchedulerError

import pytest


@pytest.mark.parametrize('exc', 
    [Exception,
     TypeError,
     StopAsyncIteration,
     StopIteration,
     ImportError,
     OSError,
     EOFError,
     RuntimeError,
     NameError,
     AttributeError,
     SyntaxError,
     LookupError,
     ValueError,
#     AssertionError,  # This one is manually allowed for testing
                       # See below for its explicit testing
     ArithmeticError,
     SystemError,
     ReferenceError,
     MemoryError,
     BufferError,
     Warning,
    ])
def test_raised_exceptions(exc):
    """None of these errors should propergate up from a task"""
    async def exception_raising():
        raise exc

    main_loop = MainLoop({}) 

    with pytest.raises(SchedulerError):
        main_loop.run_forever([exception_raising])

@pytest.mark.parametrize('exc', 
    [BaseException,
     GeneratorExit,
     SystemExit,
     KeyboardInterrupt
    ])
def test_raised_base_exceptions(exc):
    """Limited set of exceptions that are allow to be raised up from a task"""
    async def base_exception_raising():
        raise exc

    main_loop = MainLoop({}) 

    with pytest.raises(exc):
        main_loop.run_forever([base_exception_raising])


def test_raised_asserts():
    """asserts are used for testing so explicitly check this case"""
    async def assert_check():
        assert False

    main_loop = MainLoop({}) 

    with pytest.raises(AssertionError):
        main_loop.run_forever([assert_check])


@pytest.mark.parametrize('obj', [None, [], {}, (), object()])
def test_yield_unknown(obj):
    main_loop = MainLoop({}) 

    with pytest.raises(SchedulerError):
        main_loop.run_forever([])


@pytest.mark.parametrize('obj', [[], (), object()])
def test_return_unknown(obj):
    async def unknown_return():
        return obj

    main_loop = MainLoop({}) 

    with pytest.raises(SchedulerError):
        main_loop.run_forever([unknown_return])


@pytest.mark.parametrize('obj', [None, dict])
def test_return_known(obj):
    async def known_return():
        return obj

    main_loop = MainLoop({}) 

    with pytest.raises(SchedulerError):
        main_loop.run_forever([known_return])
