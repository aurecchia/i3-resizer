#!/usr/bin/env python3
""" i3 directional resizer

A script to resize windows directionally in i3.

Usage:
  i3-resizer (up | right | down | left)
  i3-resizer -h | --help

Written by Alessio Aurecchia <alessio@aurecchia.ch>

"""

import i3ipc
import sys


STEP = '20 px or 10 ppt'

i3 = i3ipc.Connection()

opposite = {
    'left': 'right',
    'up': 'down',
    'right': 'left',
    'down': 'up'
}


def print_usage():
    print("i3 directional resizer")
    print()
    print("Usage:")
    print("  i3-resizer (up | right | down | left)")
    print("  i3-resizer -h | --help")
    print()


def blocked_sides():
    focused = i3.get_tree().find_focused()

    win = focused.rect
    screen = focused.workspace().rect

    sides = ''
    if win.x <= screen.x:
        sides += 'left,'
    if win.x + win.width >= screen.x + screen.width:
        sides += 'right,'
    if win.y <= screen.y:
        sides += 'up,'
    if win.y + win.height >= screen.y + screen.height:
        sides += 'down'

    return sides


def main():
    if len(sys.argv) != 2:
        print_usage()
        exit(-1)

    arg = sys.argv[1]
    if arg in ('-h', '--help') or arg not in ('up', 'down', 'left', 'right'):
        print_usage()
        exit()

    direction = sys.argv[1]
    blocked = blocked_sides()

    if direction not in blocked and opposite[direction] not in blocked:
        action = 'grow' if direction in ('right', 'down') else 'shrink'
        axis = 'width' if direction in ('right', 'left') else 'height'

    elif direction not in blocked:
            action = 'grow'
            axis = direction

    # Window is shrinking towards border
    elif opposite[direction] not in blocked:
        action = 'shrink'
        axis = opposite[direction]

    i3.command('resize {} {} {}'.format(action, axis, STEP))


if __name__ == '__main__':
    main()

