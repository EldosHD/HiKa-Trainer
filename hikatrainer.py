#!/usr/bin/python3

import argparse
import curses
from curses.textpad import Textbox, rectangle
import random
from typing import Tuple


ver = "1.0.4"
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


def getChar(args: argparse.Namespace, series: dict, usedChars: list, unusedChars: list, k: str = "") -> str:
    """Returns a random character from the series and the key of the character. series is a dict with the keys being the keys and the values being the characters. k is the key of the last character."""
    # get random key
    while True:
        key = list(series.keys())[random.randint(0, len(series)-1)]
        if args.no_true_shuffle:
            if key != k and key not in usedChars:
                usedChars.append(key)
                unusedChars.remove(key)
                break
        elif key != k:
            break
    return series[key], key, usedChars, unusedChars


def main(stdscr: curses.window, args: argparse.Namespace, series: dict) -> Tuple[int, int]:
    remainingRepeats = args.repeat
    usedChars = []
    unusedChars = list(series.keys())
    inputString = ""
    won = False
    timesWon = 0
    timesPlayed = 0
    # get random key
    c, k, usedChars, unusedChars = getChar(args, series, usedChars=usedChars, unusedChars=unusedChars) 
    # resetting charlists for the beginning
    usedChars = []
    unusedChars = list(series.keys())
    try:
        while True:
            if remainingRepeats == 0:
                break
            if args.no_true_shuffle and len(unusedChars) == 0:
                unusedChars = list(series.keys())
                usedChars = []
            # c = character, k = key, usedChars = list of used characters, unusedChars = list of unused characters
            c, k, usedChars, unusedChars = getChar(
                args, series, usedChars, unusedChars, k)
            stdscr.clear()
            stdscr.addstr(0, 0, "Press ctrl + c to quit")
            stdscr.addstr(
                2, 0, f"You have won {timesWon} out of {timesPlayed} times")
            stdscr.addstr(4, 0, f"Enter the name of {c}")
            if args.debug:
                stdscr.addstr(
                    4, 50, f"DEBUG: k: {k}, c: {c}, lastInput: {inputString}, won: {won}")
                stdscr.addstr(5, 50, f"DEBUG: usedChars: {usedChars} unusedChars: {unusedChars}")
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
    parser.add_argument(
        '--no-true-shuffle', help='let all the characters be asked before a character is repeated', action='store_true')
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
