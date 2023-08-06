#!/usr/bin/env python3

from argparse import ArgumentParser
from collections import namedtuple
from blessed import Terminal
from time import sleep, time as now
from random import randint
from .. import common
from ..protocol import ClientEntityUpdate, ServerEntityUpdate, Messages, Direction
from ..logging import log

import socket
import pyudev
import evdev
import sys

class Point(namedtuple("Point", "x y")):
    @property
    def up(self):
        return self.__class__(self.x, self.y-1)
        
    @property
    def down(self):
        return self.__class__(self.x, self.y+1)
        
    @property
    def left(self):
        return self.__class__(self.x-1, self.y)
        
    @property
    def right(self):
        return self.__class__(self.x+1, self.y)

    def within(self, topleft, bottomright):
        x = max(self.x, topleft.x + 1)
        x = min(x, bottomright.x - 1)
        y = max(self.y, topleft.y + 1)
        y = min(y, bottomright.y - 1)

        return self.__class__(x, y)

FRAME_RATE = 10
FRAME_DELAY = 1/FRAME_RATE
PLAYER = "@"
GRASS = "^"
STAIRS_UP = ">"
STAIRS_DOWN = "<"

PLAYER_ENTITY = 0

DEADZONE = 0.15

def border(term: Terminal, topleft: Point, bottomright: Point):
    output = ""
    output += term.move_xy(topleft.x, topleft.y)
    output += "-" * (bottomright.x - topleft.x + 1)
    for i in range(topleft.y +1, bottomright.y):
        output += term.move_xy(topleft.x, i)
        output += "|"
        output += term.move_x(bottomright.x)
        output += "|"
    output += term.move_xy(topleft.x, bottomright.y)
    output += "-" * (bottomright.x - topleft.x + 1)

    print(output)

def main():
    args = ArgumentParser()
    args.add_argument('-d', '--device',
        default=[], action='append',
        help="Path to joystick/controlers to use as input (default: listen on all input devices)")
    args.add_argument('-a', '--address', default=common.DEFAULT_ADDR,
        help='Path to bind to (Default "%(default)s")')
    options = args.parse_args()

    options.device = options.device or evdev.list_devices()
    
    controllers = []
    context = pyudev.Context()
    for device in options.device:
        dev_info = pyudev.Devices.from_device_file(context, device)
        if 'ID_INPUT_JOYSTICK' in dev_info:
            controllers.append(evdev.InputDevice(device))

    for dev in controllers:
        log.info("Found input Device {dev.name}", dev=dev)

    try:
        server = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
        log.info("Connecting to {address}", address=options.address)
        server.connect(options.address)
    except FileNotFoundError:
        log.info("Unable to connect to server, server not running")
        sys.exit(1)
    log.info("Connected")
    server.setblocking(False)
    server_msgs = Messages(server)

    term = Terminal()
#    print(term.width, term.height)
    topleft = Point(term.width//4, term.height//4)
    bottomright = Point((term.width//4)*3, (term.height//4)*3)

    player_position = Point(term.width//2, term.height//2)
    command_queue = []
    
    game_state = {}
    try:
        for msg_id, update in server_msgs.recv_queue():
            log.info("Recived update from server")
            entity, direction = ServerEntityUpdate.unpack(update)
            log.info(f"Move {entity} in {Direction(direction).name}", entity=entity, Direction=Direction, direction=direction)
    except BlockingIOError:
        log.info("Bad hack hit, no updates and therefore skipping")

    grasses = []
    for i in range(20):
        x = randint(topleft.x + 1, bottomright.x - 1)
        y = randint(topleft.y + 1, bottomright.y - 1)
        grasses.append((x, y))
    x = randint(topleft.x + 1, bottomright.x - 1)
    y = randint(topleft.y + 1, bottomright.y - 1)
    entry = (x, y)
    x = randint(topleft.x + 1, bottomright.x - 1)
    y = randint(topleft.y + 1, bottomright.y - 1)
    exit = (x, y)

    with term.hidden_cursor(), term.cbreak(), term.location():
        last_loop = now()
        while True:
            # render
            print(term.clear(), end='')
            border(term, topleft, bottomright)
            for x, y in grasses:
                print(term.move_xy(x, y) + term.bold_green(GRASS), end="")
            print(term.move_xy(*entry) + term.bold_white(STAIRS_DOWN), end="")
            print(term.move_xy(*exit) + term.bold_white(STAIRS_UP), end="")
                
            print(term.move_xy(*player_position) + term.bold_red(PLAYER), end="")
            print(term.move_xy(0, bottomright.y + 1) + term.bold_white("Logs:"), flush=False)
#            print("\n".join(logs), end="") # we use join as we want to ommit trailing newline
#                                           # as a newline at end of term destroys formatting
            print(flush=True)

            # pace frames
            cur_loop = now()
            if (last_loop + FRAME_DELAY) > cur_loop:
                sleep((last_loop + FRAME_DELAY) - cur_loop)
            last_loop = cur_loop

            from select import select
            active, _, __ = select([sys.stdin] + [x.fileno() for x in controllers], [], [])
            x_direction = None
            y_direction = None
            direction = None
            keypress = 'CONTINUE'
            for controller in controllers:
                for axis in (evdev.ecodes.ABS_X, evdev.ecodes.ABS_HAT0X):
                    a = controller.absinfo(axis)
                    mid_point = (a.min + a.max) / 2
                    half_throw = a.max - mid_point
                    if a.value < (mid_point - a.flat - (half_throw * DEADZONE)):
                        x_direction = Direction.LEFT
                    elif a.value > (mid_point + a.flat + (half_throw * DEADZONE)):
                        x_direction = Direction.RIGHT
                for axis in (evdev.ecodes.ABS_Y, evdev.ecodes.ABS_HAT0Y):
                    a = controller.absinfo(axis)
                    mid_point = (a.min + a.max) / 2
                    half_throw = a.max - mid_point
                    if a.value < (mid_point - a.flat - (half_throw * DEADZONE)):
                        y_direction = Direction.UP
                    elif a.value > (mid_point + a.flat + (half_throw * DEADZONE)):
                        y_direction = Direction.DOWN
                # set default
                direction = x_direction or y_direction 
                if x_direction and y_direction:
                    if abs(x_direction) < abs(y_direction):
                        direction = x_direction
                    else:
                        direction = y_direction

                # Buttons
                keys = controller.active_keys()
                if evdev.ecodes.BTN_START in keys:
                    keypress = 'q'
                if evdev.ecodes.BTN_A in keys:
                    keypress = 'enter'
                if evdev.ecodes.BTN_B in keys:
                    keypress = 'q'
            
            if sys.stdin in active:
                # handle input
                # last key press in sample period wins
                # we read one char then try and update
                # until we run out of things to read
                # that vaule is what is processed
                char = term.inkey()
                while char:
                    keypress = char
                    char = term.inkey(timeout=0)

                direction = {
                    term.KEY_UP: Direction.UP,
                    term.KEY_DOWN: Direction.DOWN,
                    term.KEY_LEFT: Direction.LEFT,
                    term.KEY_RIGHT: Direction.RIGHT,
                }.get(keypress.code, None)

            # Buttons
            if keypress == 'q':
                break

            # Directions
            if direction == Direction.UP:
                player_position = player_position.up
                command_queue.append((1, ClientEntityUpdate.pack(PLAYER_ENTITY, Direction.UP)))
            if direction == Direction.DOWN:
                player_position = player_position.down
                command_queue.append((1, ClientEntityUpdate.pack(PLAYER_ENTITY, Direction.DOWN)))
            if direction == Direction.LEFT:
                player_position = player_position.left
                command_queue.append((1, ClientEntityUpdate.pack(PLAYER_ENTITY, Direction.LEFT)))
            if direction == Direction.RIGHT:
                player_position = player_position.right
                command_queue.append((1, ClientEntityUpdate.pack(PLAYER_ENTITY, Direction.RIGHT)))

            player_position = player_position.within(topleft, bottomright)

            # update server
            server_msgs.send_queue(command_queue)
            command_queue = []
            # recive updates
            try:
                updates = server_msgs.recv_queue()
                for msg_id, update in updates:
#                    log.info("Recived update from server")
                    entity, direction = ServerEntityUpdate.unpack(update)
#                    log.info(f"Move {entity} in {Direction(direction).name}", entity=entity, Direction=Direction, direction=direction)
            except BlockingIOError:
#                log.info("Bad hack hit, no updates and therefore skipping")
                pass

    print(term.normal)
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
