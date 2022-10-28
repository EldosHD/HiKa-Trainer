#!/usr/bin/python3

import argparse
import curses
from curses.textpad import Textbox, rectangle
import random
from typing import Tuple


ver = "1.0.3"
author = "EldosHD"
description = f"""
TODO: Insert description

Example:
hikatrainer.py --series ka ga
This command would let you train the ka and ga series.

"""
epilog = f"""
Author: {author}
Version: {ver}
License: GPLv3+
"""

aSeries = {'a': 'あ', 'i': 'い', 'u': 'う', 'e': 'え', 'o': 'お'}
kaSeries = {'ka': 'か', 'ki': 'き', 'ku': 'く', 'ke': 'け', 'ko': 'こ'}
gaSeries = {'ga': 'が', 'gi': 'ぎ', 'gu': 'ぐ', 'ge': 'げ', 'go': 'ご'}

choices = ['a', 'ka', 'ga']
defaulSeries = ['a']


def getChar(series: dict, k: str = "") -> str:
    # get random key
    while True:
        key = list(series.keys())[random.randint(0, len(series)-1)]
        if key != k:
            break
    return series[key], key


def main(stdscr: curses.window, args: argparse.Namespace, series: dict) -> Tuple[int, int]:
    remainingRepeats = args.repeat
    inputString = ""
    won = False
    timesWon = 0
    timesPlayed = 0
    c, k = getChar(series)  # c = character, k = key
    try:
        while True:
            if remainingRepeats == 0:
                break
            c, k = getChar(series=series, k=k)  # get new character and key
            stdscr.clear()
            stdscr.addstr(0, 0, "Press ctrl + c to quit")
            stdscr.addstr(2, 0, f"You have won {timesWon} out of {timesPlayed} times")
            stdscr.addstr(4, 0, f"Enter the name of {c}")
            if args.debug:
                stdscr.addstr(
                    4, 50, f"DEBUG: k: {k}, c: {c}, lastInput: {inputString}, won: {won}")
            stdscr.addstr(
                6, 0, "Enter your answer (send answer with ctrl + g): ")

            # rectangle surrounds the input field
            rectangle(stdscr, 7, 0, 9, 31)
            editwin = curses.newwin(1, 30, 8, 1)

            stdscr.refresh()

            box = Textbox(editwin)
            box.edit()
            inputString = box.gather().lower().strip()

            # check if input is correct
            if inputString == k:
                won = True
                inputString = ""
                timesWon += 1

            if won:
                stdscr.clear()
                stdscr.addstr(0, 0, "That was correct!", curses.A_BOLD)
                stdscr.addstr(1, 0, "Press any key to continue")
                stdscr.getch()
                won = False
            else:
                stdscr.clear()
                stdscr.addstr(0, 0, f"That was wrong!", curses.A_BOLD)
                stdscr.addstr(1, 0, f"The correct answer to {c} was {k}")
                stdscr.addstr(2, 0, "Press any key to continue")
                stdscr.getch()

            remainingRepeats -= 1
            timesPlayed += 1
    except KeyboardInterrupt:
        pass
    return timesWon, timesPlayed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=description, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '-s', '--series', help=f'series to train. The default is {defaulSeries}', choices=choices, nargs='+', default=defaulSeries)
    parser.add_argument(
        '-r', '--repeat', help='how often the training should be repeated. Default is 10. If this value is set to a negative number it will repeat until you cancel the program', type=int, default=10)
    parser.add_argument(
        '-d', '--debug', help='Enable debug mode', action='store_true')
    parser.add_argument(
        '-v', '--verbose', help='increase output verbosity', action='count', default=0)
    parser.add_argument('-V', '--version', action='version',
                        version=f'%(prog)s {ver}')

    args = parser.parse_args()

    series = {}
    for s in args.series:
        if s == 'a':
            series.update(aSeries)
        elif s == 'ka':
            series.update(kaSeries)
        elif s == 'ga':
            series.update(gaSeries)

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    timesWon, timesPlayed = curses.wrapper(main, args, series)
    print(f"You won {timesWon} out of {timesPlayed} times!")
