#!/usr/bin/python3

import argparse
import curses
from curses.textpad import Textbox, rectangle

ver = "0.0.1"
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

aSeries = {'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o'}
kaSeries = {'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko'}
gaSeries = {'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go'}

choices = ['a', 'ka', 'ga']
defaulSeries = ['a']

def getChar():
    return aSeries['あ']

def main(stdscr,args):
    remainingRepeats = args.repeat
    inputString = ""
    try:
        while True:
            if remainingRepeats <= 0:
                break
            c = getChar()
            stdscr.clear()
            stdscr.addstr(0, 0, "Press ctrl + c to quit")
            stdscr.addstr(2, 0, f"Remaining repeats: {remainingRepeats}")
            stdscr.addstr(4, 0, f"Enter the name of {c}")
            stdscr.addstr(6, 0, "Enter your answer (send answer with ctrl + g): ")

            # rectangle surrounds the input field
            rectangle(stdscr, 7,0, 13,31)
            editwin = curses.newwin(5,30, 8,1)

            stdscr.refresh()

            box = Textbox(editwin)
            box.edit()
            inputString = box.gather()
            remainingRepeats -= 1
    except KeyboardInterrupt:
        pass 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('-s', '--series', help='Series to train', choices=choices, nargs='+', default=defaulSeries)
    parser.add_argument('-r', '--repeat', help='how often the training should be repeated. Default is 10', type=int, default=10)
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='count', default=0)
    parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {ver}') 

    args = parser.parse_args()

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    curses.wrapper(main, args)