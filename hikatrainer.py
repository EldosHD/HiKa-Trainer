#!/usr/bin/python3

import argparse
import curses
from curses.textpad import Textbox, rectangle
import random
from typing import Tuple
from collections import Counter


ver = "1.1.6"
author = "EldosHD"
description = f"""
TODO: Insert description

Example:
hikatrainer.py --series ka ga
This command would let you train the ka and ga series.

hikatrainer.py --all
This command would let you train every series. 

"""
epilog = f"""
Author: {author}
Version: {ver}
License: GPLv3+
"""

aSeries = {'a': 'あ', 'i': 'い', 'u': 'う', 'e': 'え', 'o': 'お'}
kaSeries = {'ka': 'か', 'ki': 'き', 'ku': 'く', 'ke': 'け', 'ko': 'こ'}
gaSeries = {'ga': 'が', 'gi': 'ぎ', 'gu': 'ぐ', 'ge': 'げ', 'go': 'ご'}
saSeries = {'sa': 'さ', 'shi': 'し', 'su': 'す', 'se': 'せ', 'so': 'そ'}
zaSeries = {'za': 'ざ', 'ji': 'じ', 'zu': 'ず', 'ze': 'ぜ', 'zo': 'ぞ'}
taSeries = {'ta': 'た', 'chi': 'ち', 'tsu': 'つ', 'te': 'て', 'to': 'と'}
daSeries = {'da': 'だ', 'ji': 'ぢ', 'zu': 'づ', 'de': 'で', 'do': 'ど'}
naSeries = {'na': 'な', 'ni': 'に', 'nu': 'ぬ', 'ne': 'ね', 'no': 'の'}
haSeries = {'ha': 'は', 'hi': 'ひ', 'fu': 'ふ', 'he': 'へ', 'ho': 'ほ'}
baSeries = {'ba': 'ば', 'bi': 'び', 'bu': 'ぶ', 'be': 'べ', 'bo': 'ぼ'}
paSeries = {'pa': 'ぱ', 'pi': 'ぴ', 'pu': 'ぷ', 'pe': 'ぺ', 'po': 'ぽ'}
maSeries = {'ma': 'ま', 'mi': 'み', 'mu': 'む', 'me': 'め', 'mo': 'も'}
yaSeries = {'ya': 'や', 'yu': 'ゆ', 'yo': 'よ'}
raSeries = {'ra': 'ら', 'ri': 'り', 'ru': 'る', 're': 'れ', 'ro': 'ろ'}
waSeries = {'wa': 'わ', 'wo': 'を'}
nSeries = {'n': 'ん'}

kySeries = {'kya': 'きゃ', 'kyu': 'きゅ', 'kyo': 'きょ'}
gySeries = {'gya': 'ぎゃ', 'gyu': 'ぎゅ', 'gyo': 'ぎょ'}
shSeries = {'sha': 'しゃ', 'shu': 'しゅ', 'sho': 'しょ'}
jSeries = {'ja': 'じゃ', 'ju': 'じゅ', 'jo': 'じょ'}
chSeries = {'cha': 'ちゃ', 'chu': 'ちゅ', 'cho': 'ちょ'}
nySeries = {'nya': 'にゃ', 'nyu': 'にゅ', 'nyo': 'にょ'}
hySeries = {'hya': 'ひゃ', 'hyu': 'ひゅ', 'hyo': 'ひょ'}
bySeries = {'bya': 'びゃ', 'byu': 'びゅ', 'byo': 'びょ'}
pySeries = {'pya': 'ぴゃ', 'pyu': 'ぴゅ', 'pyo': 'ぴょ'}
mySeries = {'mya': 'みゃ', 'myu': 'みゅ', 'myo': 'みょ'}
rySeries = {'rya': 'りゃ', 'ryu': 'りゅ', 'ryo': 'りょ'}

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
    wrongChars = []
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
                stdscr.addstr(20, 0, f"DEBUG: usedChars: {usedChars}")
                stdscr.addstr(22, 0, f"DEBUG: unusedChars: {unusedChars}")
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
                wrongChars.append(k)

                stdscr.clear()
                stdscr.addstr(0, 0, f"That was wrong!", curses.A_BOLD)
                stdscr.addstr(1, 0, f"The correct answer to {c} was {k}")
                stdscr.addstr(2, 0, "Press any key to continue")
                stdscr.getch()

            remainingRepeats -= 1
            timesPlayed += 1
    except KeyboardInterrupt:
        pass
    return timesWon, timesPlayed, wrongChars


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=description, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)

    # general options
    general = parser.add_argument_group("general options")
    general.add_argument(
        '-d', '--debug', help='Enable debug mode', action='store_true')
    general.add_argument(
        '-v', '--verbose', help='increase output verbosity', action='count', default=0)
    general.add_argument(
        '--no-true-shuffle', help='let all the characters be asked before a character is repeated', action='store_true')
    general.add_argument('-V', '--version', action='version',
                        version=f'%(prog)s {ver}')
    # repeat options
    repeat = general.add_mutually_exclusive_group()
    repeat.add_argument(
        '-r', '--repeat', help='how often the training should be repeated. Default is 10. If this value is set to a negative number it will repeat until you cancel the program', type=int, default=10)
    repeat.add_argument('-e', '--endless', help='repeat until you cancel the program. This is the same as "-r -1"', action='store_true')

    # series options
    seriesGroup = parser.add_mutually_exclusive_group()
    seriesGroup.add_argument(
        '-s', '--series', help=f'series to train. If no series option is given this will use the default series. The default is {defaulSeries}', nargs='+', default=defaulSeries)
    seriesGroup.add_argument('-a', '--all', help='train all series', action='store_true')
    seriesGroup.add_argument('-c', '--custom', help='train a custom series. This option takes a list of characters. If you want to use a space in a character you have to use a backslash before the space. Example: "a b c" -> "a\\ b\\ c"', nargs='+')
    seriesGroup.add_argument('-l', '--list', help='list every possible series', action='store_true')

    args = parser.parse_args()

    if args.endless:
        args.repeat = -1

    # check which series to use
    series = {}
    if args.all:
        series = {**aSeries, **kaSeries, **saSeries, **taSeries, **naSeries, **haSeries, **maSeries, **yaSeries, **raSeries, **waSeries, **gaSeries, **zaSeries, **daSeries, **baSeries, **paSeries, **kySeries, **shSeries, **chSeries, **nySeries, **hySeries, **bySeries, **pySeries, **mySeries, **rySeries}
    elif args.list:
        print("The following series are available:")
        print("a, ka, sa, ta, na, ha, ma, ya, ra, wa, ga, za, da, ba, pa, kya, sha, cha, nya, hya, bya, pya, mya, rya")
        exit(0)
    elif args.custom:
        for char in args.custom:
            char = char.replace("\\ ", " ")
            allSeries = {**aSeries, **kaSeries, **saSeries, **taSeries, **naSeries, **haSeries, **maSeries, **yaSeries, **raSeries, **waSeries, **gaSeries, **zaSeries, **daSeries, **baSeries, **paSeries, **kySeries, **shSeries, **chSeries, **nySeries, **hySeries, **bySeries, **pySeries, **mySeries, **rySeries}
            if char in allSeries:
                series[char] = allSeries[char]
            else:
                print(f'Character "{char}" not found')
                exit(1)
    else:
        for s in args.series:
            if s == 'a':
                series.update(aSeries)
            elif s == 'ka':
                series.update(kaSeries)
            elif s == 'ga':
                series.update(gaSeries)
            elif s == 'sa':
                series.update(saSeries)
            elif s == 'za':
                series.update(zaSeries)
            elif s == 'ta':
                series.update(taSeries)
            elif s == 'da':
                series.update(daSeries)
            elif s == 'na':
                series.update(naSeries)
            elif s == 'ha':
                series.update(haSeries)
            elif s == 'ba':
                series.update(baSeries)
            elif s == 'pa':
                series.update(paSeries)
            elif s == 'ma':
                series.update(maSeries)
            elif s == 'ya':
                series.update(yaSeries)
            elif s == 'ra':
                series.update(raSeries)
            elif s == 'wa':
                series.update(waSeries)
            elif s == 'n':
                series.update(nSeries)
            elif s == 'kya':
                series.update(kySeries)
            elif s == 'gya':
                series.update(gySeries)
            elif s == 'sha':
                series.update(shSeries)
            elif s == 'ja':
                series.update(jSeries)
            elif s == 'cha':
                series.update(chSeries)
            elif s == 'nya':
                series.update(nySeries)
            elif s == 'hya':
                series.update(hySeries)
            elif s == 'bya':
                series.update(bySeries)
            elif s == 'pya':
                series.update(pySeries)
            elif s == 'mya':
                series.update(mySeries)
            elif s == 'rya':
                series.update(rySeries)
            else:
                print(f"series {s} not found")
                exit(1)

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    timesWon, timesPlayed, wrongChars = curses.wrapper(main, args, series)
    print()
    print(f"You won {timesWon} out of {timesPlayed} times!")
    print()
    for k, v in Counter(wrongChars).items():
        print(f"{series.get(k)} ({k}) was wrong {v} times")