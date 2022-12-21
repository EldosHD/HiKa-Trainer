#!/usr/bin/python3

import argparse
import curses
from curses.textpad import Textbox, rectangle
import random
from typing import Tuple
from collections import Counter


ver = "1.3.1"
author = "EldosHD"
description = f"""
TODO: Insert description

Example:
hikatrainer.py series -s ka ga
This command would let you train the ka and ga series in hiragana.

hikatrainer.py series --all -e
This command would let you train every series in hiragana until you cancle the program with ctrl + c. 

hikatrainer.py series -s ka ga -r 100 -S katakana
This command would let you train the ka and ga series in katakana 100 times.

"""
epilog = f"""
Author: {author}
Version: {ver}
License: GPLv3+
"""

# Series
# Hiragana
aSeriesHiragana = {'a': 'あ', 'i': 'い', 'u': 'う', 'e': 'え', 'o': 'お'}
kaSeriesHiragana = {'ka': 'か', 'ki': 'き', 'ku': 'く', 'ke': 'け', 'ko': 'こ'}
gaSeriesHiragana = {'ga': 'が', 'gi': 'ぎ', 'gu': 'ぐ', 'ge': 'げ', 'go': 'ご'}
saSeriesHiragana = {'sa': 'さ', 'shi': 'し', 'su': 'す', 'se': 'せ', 'so': 'そ'}
zaSeriesHiragana = {'za': 'ざ', 'ji': 'じ', 'zu': 'ず', 'ze': 'ぜ', 'zo': 'ぞ'}
taSeriesHiragana = {'ta': 'た', 'chi': 'ち', 'tsu': 'つ', 'te': 'て', 'to': 'と'}
daSeriesHiragana = {'da': 'だ', 'ji': 'ぢ', 'zu': 'づ', 'de': 'で', 'do': 'ど'}
naSeriesHiragana = {'na': 'な', 'ni': 'に', 'nu': 'ぬ', 'ne': 'ね', 'no': 'の'}
haSeriesHiragana = {'ha': 'は', 'hi': 'ひ', 'fu': 'ふ', 'he': 'へ', 'ho': 'ほ'}
baSeriesHiragana = {'ba': 'ば', 'bi': 'び', 'bu': 'ぶ', 'be': 'べ', 'bo': 'ぼ'}
paSeriesHiragana = {'pa': 'ぱ', 'pi': 'ぴ', 'pu': 'ぷ', 'pe': 'ぺ', 'po': 'ぽ'}
maSeriesHiragana = {'ma': 'ま', 'mi': 'み', 'mu': 'む', 'me': 'め', 'mo': 'も'}
yaSeriesHiragana = {'ya': 'や', 'yu': 'ゆ', 'yo': 'よ'}
raSeriesHiragana = {'ra': 'ら', 'ri': 'り', 'ru': 'る', 're': 'れ', 'ro': 'ろ'}
waSeriesHiragana = {'wa': 'わ', 'wo': 'を'}
nSeriesHiragana = {'n': 'ん'}

kySeriesHiragana = {'kya': 'きゃ', 'kyu': 'きゅ', 'kyo': 'きょ'}
gySeriesHiragana = {'gya': 'ぎゃ', 'gyu': 'ぎゅ', 'gyo': 'ぎょ'}
shSeriesHiragana = {'sha': 'しゃ', 'shu': 'しゅ', 'sho': 'しょ'}
jSeriesHiragana = {'ja': 'じゃ', 'ju': 'じゅ', 'jo': 'じょ'}
chSeriesHiragana = {'cha': 'ちゃ', 'chu': 'ちゅ', 'cho': 'ちょ'}
nySeriesHiragana = {'nya': 'にゃ', 'nyu': 'にゅ', 'nyo': 'にょ'}
hySeriesHiragana = {'hya': 'ひゃ', 'hyu': 'ひゅ', 'hyo': 'ひょ'}
bySeriesHiragana = {'bya': 'びゃ', 'byu': 'びゅ', 'byo': 'びょ'}
pySeriesHiragana = {'pya': 'ぴゃ', 'pyu': 'ぴゅ', 'pyo': 'ぴょ'}
mySeriesHiragana = {'mya': 'みゃ', 'myu': 'みゅ', 'myo': 'みょ'}
rySeriesHiragana = {'rya': 'りゃ', 'ryu': 'りゅ', 'ryo': 'りょ'}

# Katakana
aSeriesKatakana = {'a': 'ア', 'i': 'イ', 'u': 'ウ', 'e': 'エ', 'o': 'オ'}
kaSeriesKatakana = {'ka': 'カ', 'ki': 'キ', 'ku': 'ク', 'ke': 'ケ', 'ko': 'コ'}
gaSeriesKatakana = {'ga': 'ガ', 'gi': 'ギ', 'gu': 'グ', 'ge': 'ゲ', 'go': 'ゴ'}
saSeriesKatakana = {'sa': 'サ', 'shi': 'シ', 'su': 'ス', 'se': 'セ', 'so': 'ソ'}
zaSeriesKatakana = {'za': 'ザ', 'ji': 'ジ', 'zu': 'ズ', 'ze': 'ゼ', 'zo': 'ゾ'}
taSeriesKatakana = {'ta': 'タ', 'chi': 'チ', 'tsu': 'ツ', 'te': 'テ', 'to': 'ト'}
daSeriesKatakana = {'da': 'ダ', 'ji': 'ヂ', 'zu': 'ヅ', 'de': 'デ', 'do': 'ド'}
naSeriesKatakana = {'na': 'ナ', 'ni': 'ニ', 'nu': 'ヌ', 'ne': 'ネ', 'no': 'ノ'}
haSeriesKatakana = {'ha': 'ハ', 'hi': 'ヒ', 'fu': 'フ', 'he': 'ヘ', 'ho': 'ホ'}
baSeriesKatakana = {'ba': 'バ', 'bi': 'ビ', 'bu': 'ブ', 'be': 'ベ', 'bo': 'ボ'}
paSeriesKatakana = {'pa': 'パ', 'pi': 'ピ', 'pu': 'プ', 'pe': 'ペ', 'po': 'ポ'}
maSeriesKatakana = {'ma': 'マ', 'mi': 'ミ', 'mu': 'ム', 'me': 'メ', 'mo': 'モ'}
yaSeriesKatakana = {'ya': 'ヤ', 'yu': 'ユ', 'yo': 'ヨ'}
raSeriesKatakana = {'ra': 'ラ', 'ri': 'リ', 'ru': 'ル', 're': 'レ', 'ro': 'ロ'}
waSeriesKatakana = {'wa': 'ワ', 'wo': 'ヲ'}
nSeriesKatakana = {'n': 'ン'}

kySeriesKatakana = {'kya': 'キャ', 'kyu': 'キュ', 'kyo': 'キョ'}
gySeriesKatakana = {'gya': 'ギャ', 'gyu': 'ギュ', 'gyo': 'ギョ'}
shSeriesKatakana = {'sha': 'シャ', 'shu': 'シュ', 'sho': 'ショ'}
jSeriesKatakana = {'ja': 'ジャ', 'ju': 'ジュ', 'jo': 'ジョ'}
chSeriesKatakana = {'cha': 'チャ', 'chu': 'チュ', 'cho': 'チョ'}
nySeriesKatakana = {'nya': 'ニャ', 'nyu': 'ニュ', 'nyo': 'ニョ'}
hySeriesKatakana = {'hya': 'ヒャ', 'hyu': 'ヒュ', 'hyo': 'ヒョ'}
bySeriesKatakana = {'bya': 'ビャ', 'byu': 'ビュ', 'byo': 'ビョ'}
pySeriesKatakana = {'pya': 'ピャ', 'pyu': 'ピュ', 'pyo': 'ピョ'}
mySeriesKatakana = {'mya': 'ミャ', 'myu': 'ミュ', 'myo': 'ミョ'}
rySeriesKatakana = {'rya': 'リャ', 'ryu': 'リュ', 'ryo': 'リョ'}


defaulSeries = ['a']

# words
words = {}


def getSeries(args: argparse.Namespace, series: dict) -> dict:
    returnSeries = {}
    for s in args.series:
        # TODO: solve this more elegantly
        #  make new dict --> {ka: {**kaSeriesHiragana}, ga: {**gaSeriesHiragana}} etc
        # just check for s in dict.keys() and update with dict[s] oder so?
        if s == 'a':
            if args.system == "hiragana":
                returnSeries.update(aSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(aSeriesKatakana)
        elif s == 'ka':
            if args.system == "hiragana":
                returnSeries.update(kaSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(kaSeriesKatakana)
        elif s == 'ga':
            if args.system == "hiragana":
                returnSeries.update(gaSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(gaSeriesKatakana)
        elif s == 'sa':
            if args.system == "hiragana":
                returnSeries.update(saSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(saSeriesKatakana)
        elif s == 'za':
            if args.system == "hiragana":
                returnSeries.update(zaSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(zaSeriesKatakana)
        elif s == 'ta':
            if args.system == "hiragana":
                returnSeries.update(taSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(taSeriesKatakana)
        elif s == 'da':
            if args.system == "hiragana":
                returnSeries.update(daSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(daSeriesKatakana)
        elif s == 'na':
            if args.system == "hiragana":
                returnSeries.update(naSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(naSeriesKatakana)
        elif s == 'ha':
            if args.system == "hiragana":
                returnSeries.update(haSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(haSeriesKatakana)
        elif s == 'ba':
            if args.system == "hiragana":
                returnSeries.update(baSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(baSeriesKatakana)
        elif s == 'pa':
            if args.system == "hiragana":
                returnSeries.update(paSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(paSeriesKatakana)
        elif s == 'ma':
            if args.system == "hiragana":
                returnSeries.update(maSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(maSeriesKatakana)
        elif s == 'ya':
            if args.system == "hiragana":
                returnSeries.update(yaSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(yaSeriesKatakana)
        elif s == 'ra':
            if args.system == "hiragana":
                returnSeries.update(raSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(raSeriesKatakana)
        elif s == 'wa':
            if args.system == "hiragana":
                returnSeries.update(waSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(waSeriesKatakana)
        elif s == 'n':
            if args.system == "hiragana":
                returnSeries.update(nSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(nSeriesKatakana)
        elif s == 'kya':
            if args.system == "hiragana":
                returnSeries.update(kySeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(kySeriesKatakana)
        elif s == 'gya':
            if args.system == "hiragana":
                returnSeries.update(gySeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(gySeriesKatakana)
        elif s == 'sha':
            if args.system == "hiragana":
                returnSeries.update(shSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(shSeriesKatakana)
        elif s == 'ja':
            if args.system == "hiragana":
                returnSeries.update(jSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(jSeriesKatakana)
        elif s == 'cha':
            if args.system == "hiragana":
                returnSeries.update(chSeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(chSeriesKatakana)
        elif s == 'nya':
            if args.system == "hiragana":
                returnSeries.update(nySeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(nySeriesKatakana)
        elif s == 'hya':
            if args.system == "hiragana":
                returnSeries.update(hySeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(hySeriesKatakana)
        elif s == 'bya':
            if args.system == "hiragana":
                returnSeries.update(bySeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(bySeriesKatakana)
        elif s == 'pya':
            if args.system == "hiragana":
                returnSeries.update(pySeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(pySeriesKatakana)
        elif s == 'mya':
            if args.system == "hiragana":
                returnSeries.update(mySeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(mySeriesKatakana)
        elif s == 'rya':
            if args.system == "hiragana":
                returnSeries.update(rySeriesHiragana)
            elif args.system == "katakana":
                returnSeries.update(rySeriesKatakana)
        else:
            print("Error: Invalid series: " + s)
            exit(1)
    return returnSeries


def getCustomSeries(args: argparse.Namespace, inputSeries: dict) -> dict:
    if len(args.custom) == 1:
        print('Error: Custom series must be at least 2 characters long')
        exit(1)
    series = {}
    for char in args.custom:
        char = char.replace("\\ ", " ")
        if char in series:
            print('Error: Custom series cannot contain duplicate characters')
            exit(1)
        if char in inputSeries:
            series[char] = inputSeries[char]
        else:
            system = ""
            if args.system == "hiragana":
                system = "Hiragana"
            elif args.system == "katakana":
                system = "Katakana"

            print(f'{system} Character "{char}" not found')
            exit(1)
    return series


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


def seriesTrainer(stdscr: curses.window, args: argparse.Namespace, series: dict) -> Tuple[int, int]:
    remainingRepeats = 10
    # setting remaining repeats to the length of the series if it is not set manually
    if args.repeat != None:
        remainingRepeats = args.repeat
    elif args.series_repeat != None:
        remainingRepeats = args.series_repeat * len(series)
        args.no_true_shuffle = True
    elif args.endless:
        remainingRepeats = -1
    else:
        pass
    usedChars = []
    unusedChars = list(series.keys())
    inputString = ""
    won = False
    timesWon = 0
    timesPlayed = 0
    # get random key
    c, k, usedChars, unusedChars = getChar(
        args, series, usedChars=usedChars, unusedChars=unusedChars)
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
    return timesWon, timesPlayed, wrongChars, 0, ""


def wordTrainer(stdscr: curses.window, args: argparse.Namespace):
    return 0, 0, [], 0, ""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=description, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)

    parentParser = argparse.ArgumentParser(add_help=False)

    # options for every subcommand

    # general options
    general = parentParser.add_argument_group("general options")
    general.add_argument(
        '-d', '--debug', help='Enable debug mode', action='store_true')
    general.add_argument(
        '-v', '--verbose', help='increase output verbosity', action='count', default=0)
    general.add_argument('-V', '--version', action='version',
                         version=f'{ver}')
    # repeat options
    repeat = parentParser.add_argument_group("repeat options")
    repeat.add_argument(
        '-r', '--repeat', help='how often the training should be repeated. Default is 10. If this value is set to a negative number it will repeat until you cancel the program', type=int, default=None)
    repeat.add_argument(
        '-e', '--endless', help='repeat until you cancel the program. This is the same as "-r -1"', action='store_true', default=False)

    # Subcommands
    mode = parser.add_subparsers(
        dest="mode", help="The training mode you want to use")

    seriesMode = mode.add_parser(
        "series", help="Train reading single characters", parents=[parentParser])
    wordMode = mode.add_parser(
        "word", help="Train reading words", parents=[parentParser])

    # series options
    seriesMode.add_argument('-S', '--system', help='The writing system you want to train. Default is hiragana',
                            choices=['hiragana', 'katakana'], default='hiragana')
    seriesGroup = seriesMode.add_mutually_exclusive_group()
    seriesGroup.add_argument(
        '-s', '--series', help=f'series to train. If no series option is given this will use the default series. The default is {defaulSeries}', nargs='+', default=defaulSeries)
    seriesGroup.add_argument(
        '-a', '--all', help='train all series', action='store_true')
    seriesGroup.add_argument(
        '-c', '--custom', help='train a custom series. This option takes a list of characters. If you want to use a space in a character you have to use a backslash before the space. Example: "a b c" -> "a\\ b\\ c"', nargs='+')
    seriesGroup.add_argument(
        '-l', '--list', help='list every possible series', action='store_true')

    # series specific other options
    otherOptions = seriesMode.add_argument_group("other options")
    otherOptions.add_argument(
        '--no-true-shuffle', help='let all the characters be asked before a character is repeated', action='store_true')
    otherOptions.add_argument('-R', '--series-repeat',
                              help='repeat the series a certain amount of times. This automatically activates --no-true-shuffle and overrites the other repeat options', type=int, default=None)

    # word options
    # do word options

    # parse args
    args = parser.parse_args()

    if args.mode == "series":
        # check which series to use
        allHiragana = {**aSeriesHiragana, **kaSeriesHiragana, **gaSeriesHiragana, **saSeriesHiragana, **zaSeriesHiragana, **taSeriesHiragana, **daSeriesHiragana, **naSeriesHiragana, **haSeriesHiragana, **baSeriesHiragana, **paSeriesHiragana, **maSeriesHiragana, **yaSeriesHiragana, **raSeriesHiragana, **waSeriesHiragana, **nSeriesHiragana, **kySeriesHiragana, **gySeriesHiragana, **shSeriesHiragana, **jSeriesHiragana, **chSeriesHiragana, **nySeriesHiragana, **hySeriesHiragana, **bySeriesHiragana, **pySeriesHiragana, **mySeriesHiragana, **rySeriesHiragana}
        allKatakana = {**aSeriesKatakana, **kaSeriesKatakana, **gaSeriesKatakana, **saSeriesKatakana, **zaSeriesKatakana, **taSeriesKatakana, **daSeriesKatakana, **naSeriesKatakana, **haSeriesKatakana, **baSeriesKatakana, **paSeriesKatakana, **maSeriesKatakana, **yaSeriesKatakana, **raSeriesKatakana, **waSeriesKatakana, **nSeriesKatakana, **kySeriesKatakana, **gySeriesKatakana, **shSeriesKatakana, **jSeriesKatakana, **chSeriesKatakana, **nySeriesKatakana, **hySeriesKatakana, **bySeriesKatakana, **pySeriesKatakana, **mySeriesKatakana, **rySeriesKatakana}
        series = {}
        if args.all:
            if args.system == "hiragana":
                series = allHiragana
            elif args.system == "katakana":
                series = allKatakana
            else:
                print("Error: Unknown system")
                exit(1)
        elif args.list:
            print("The following series are available:")
            print("a, ka, ga, sa, za, ta, da, na, ha, ba, pa, ma, ya, ra, wa, n, kya, gya, sha, ja, cha, nya, hya, bya, pya, mya, rya")
            exit(0)
        elif args.custom:
            if args.system == "hiragana":
                series = getCustomSeries(args, allHiragana)
            elif args.system == "katakana":
                series = getCustomSeries(args, allKatakana)
            else:
                print("Invalid system")
                exit(1)
        else:
            if args.system == "hiragana":
                series = getSeries(args, allHiragana)
            elif args.system == "katakana":
                series = getSeries(args, allKatakana)
            else:
                print("Invalid system")
                exit(1)
    elif args.mode == "word":
        pass
    else:
        parser.print_help()
        exit(1)

    if args.endless:
        args.repeat = -1

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # set variables
    timesWon, timesPlayed, wrongChars, exitCode, exitMsg = 0, 0, [], 0, ""

    # start the given mode
    if args.mode == "series":
        timesWon, timesPlayed, wrongChars, exitCode, exitMsg = curses.wrapper(
            seriesTrainer, args, series)
    elif args.mode == "word":
        timesWon, timesPlayed, wrongChars, exitCode, exitMsg = curses.wrapper(
            wordTrainer, args)
    else:
        print("No system selected")
        exit(1)

    # print error message if there is one
    if exitCode == 1:
        print(exitMsg)
        exit(1)

    print()
    print(f"You won {timesWon} out of {timesPlayed} times!")
    print()
    for k, v in Counter(wrongChars).items():
        print(f"{series.get(k)} ({k}) was wrong {v} times")
