#!/usr/bin/python3

import argparse
import curses
from curses.textpad import Textbox, rectangle
import random


ver = "1.0.0"
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

def getChar(series: dict) -> str:
    # get random key
    key = list(series.keys())[random.randint(0, len(series)-1)]
    return series[key], key

def main(stdscr: curses.window, args: argparse.Namespace, series: dict):
    remainingRepeats = args.repeat
    inputString = ""
    won = False
    timesWon = 0
    try:
        while True:
            if remainingRepeats <= 0:
                break
            if won:
                stdscr.clear()
                stdscr.addstr(0, 0, "That was correct!")
                stdscr.addstr(1, 0, "Press any key to continue")
                stdscr.getch()
                won = False
            c,k = getChar(series=series)
            stdscr.clear()
            stdscr.addstr(0, 0, "Press ctrl + c to quit")
            stdscr.addstr(2, 0, f"Remaining repeats: {remainingRepeats}")
            stdscr.addstr(4, 0, f"Enter the name of {c}")
            if args.debug:
                stdscr.addstr(4, 50, f"DEBUG: k: {k}, c: {c}, lastInput: {inputString}, won: {won}")
            stdscr.addstr(6, 0, "Enter your answer (send answer with ctrl + g): ")

            # rectangle surrounds the input field
            rectangle(stdscr, 7,0, 13,31)
            editwin = curses.newwin(5,30, 8,1)

            stdscr.refresh()

            box = Textbox(editwin)
            box.edit()
            inputString = box.gather().lower().strip()
            if inputString == k:
                won = True
                inputString = ""
                timesWon += 1
 
            remainingRepeats -= 1
    except KeyboardInterrupt:
        pass
    return timesWon

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('-s', '--series', help='Series to train', choices=choices, nargs='+', default=defaulSeries)
    parser.add_argument('-r', '--repeat', help='how often the training should be repeated. Default is 10', type=int, default=10)
    parser.add_argument('-d', '--debug', help='Enable debug mode', action='store_true')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='count', default=0)
    parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {ver}') 

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

    timesWon = curses.wrapper(main, args, series)
    print(f"You won {timesWon} times!")