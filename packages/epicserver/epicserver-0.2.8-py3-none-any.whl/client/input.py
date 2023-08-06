#!/usr/bin/env python3

from pyudev import Context, Monitor, Devices
from functools import partial
from contextlib import suppress
from select import select
from fcntl import fcntl, F_SETFL
from errno import ENODEV
import evdev
import sys
import os

context = Context()
udev_monitor = Monitor.from_netlink(context)
nonblock_monitor = partial(udev_monitor.poll, timeout=0)
udev_monitor.filter_by('input')
udev_monitor.start()

# write this loop to update shared mutable state
# mustable state should be 'intentions' and not button pushes
# need to map button pushes per input device to intentions


class InputMux():
    def __init__(self, mapping={}):
        self.gamepads = {}
        self.current_state = {}
        self.mapping = mapping or {} # key = device, key
        
        self.setup_gamepads()
        self.setup_stdin()

    # blocking
    def read():
        pass

    # non blocking
    def get_state():
        pass

    def setup_gamepads(self):
        gamepads = {}

        print("Auto-Detected Gamepads (evdev/udev):")
        for gamepad_dev in evdev.list_devices():
            gamepad_udev = Devices.from_device_file(context, gamepad_dev)
            if 'ID_INPUT_JOYSTICK' in gamepad_udev:
                gamepad = evdev.InputDevice(gamepad_dev)
                gamepads[gamepad.fileno()] = gamepad
                print(" *", gamepad)

        self.gamepads = gamepads

    def setup_stdin(self):
        print("Adding STDIN as an input device")
        ret = fcntl(sys.stdin.fileno(), F_SETFL, os.O_NONBLOCK)
        assert not ret, 'Could not set stdin to O_NONBLOCK, fallback input device would not work'

    def __call__(self):
        """Self contained logic to read input and update state, normmaly used in a thread"""
        while True:
            gamepad_filenos = gamepads.keys()
            gamepad_filenos = list(gamepad_filenos)
            rd, _, __ = select([udev_monitor.fileno(), sys.stdin.fileno()] + gamepad_filenos, [], [])
            for device in iter(nonblock_monitor, None):
                if 'ID_INPUT_JOYSTICK' in device:
                    if device.action == 'add':
                        event_devices = evdev.list_devices()
                        # Is this a evdev device and not hidraw or JS
                        if device.device_node in event_devices:
                            print('add', device.action, device.sys_name, device.device_path)
                            gamepad = evdev.InputDevice(device.device_node)
                            gamepads[gamepad.fileno()] = gamepad
                    # turns out the fd goes readable and reading returns an OS Errror
                    # see handling in event layer below
                    #elif device.action == 'remove':
                    else:
                        print(device.action, device.sys_name, 'not handling')

            # process input
            # copy dictonary as we MAY mutate it to delete old devices
            for fileno, device in list(gamepads.items()):
                try:
                    if fileno in rd:
                        for event in device.read():
                            print('evdev:', event)
                except OSError as err:
                    if err.errno == ENODEV:
                        print("Removing device as it is unresponseive:", device)
                        del gamepads[fileno]
                    

            if sys.stdin.fileno() in rd:
                char = sys.stdin.read(1)
                while char:
                    print(f'stdin: "{char}"')
                    char = sys.stdin.read(1)

# utils for midpoint (abs -> button conversion)
#            keys = controller.active_keys()
#            a = controller.absinfo(axis)
#            mid_point = (a.min + a.max) / 2
#            half_throw = a.max - mid_point
#            if a.value < (mid_point - a.flat - (half_throw * DEADZONE)):
#                x_direction = Direction.LEFT
#            elif a.value > (mid_point + a.flat + (half_throw * DEADZONE)):
#                x_direction = Direction.RIGHT a
#
