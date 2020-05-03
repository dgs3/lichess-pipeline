#!/usr/bin/env python3.7
"""Module to determine the win/loss rate of certain openings.

This script prints the data in the format of:

$OPENING_NAME:
    Wins:
    Losses:
    Draws:
...
"""

import enum

import util


class Result(enum.Enum):
    """Enum to hold game results."""
    WIN = 'win'
    LOSS = 'loss'
    DRAW = 'draw'
    # I'm not sure what the difference between these is. Could be lichess isn't
    # very strict with the results field.
    TIMEOUT = 'timeout'
    OUT_OF_TIME = 'outoftime'


def get_game_data(game_dict, player) -> tuple:
    """Parses some game data from a lichess game dict."""
    opening_name = util.get_opening_name(game_dict)
    if game_dict['status'] == Result.DRAW.value:
        return (opening_name, Result.DRAW)
    winner_name = util.get_game_winner(game_dict)
    return (opening_name, Result.WIN if winner_name == player else Result.LOSS)


def opening_table_to_str(opening_table) -> str:
    """Format an opening table to markdown."""
    to_return = ""
    for opening_name, data in opening_table.items():
        to_add = [
            f'{opening_name}:\n',
            f'    Wins: {data[Result.WIN]}\n',
            f'    Losses: {data[Result.LOSS]}\n',
            f'    Draws: {data[Result.DRAW]}\n',
        ]
        to_return += ' '.join(to_add)
    return to_return


def game_is_timeout(game_dict) -> bool:
    """Returns True if this game is a timeout. False otherwise.

    For some reason lichess doesn't keep winner data on timeout games.
    :shrug:.
    """
    return game_dict['status'] in [
        Result.TIMEOUT.value, Result.OUT_OF_TIME.value
    ]


def ignore_game(game_dict) -> bool:
    """Returns True if we should just ignore this game data. False otherwise.

    We ignore some games if they have insufficient date.
    """
    return not util.game_has_opening_data(game_dict) or game_is_timeout(
        game_dict)


def analyze_games(game_data, player) -> str:
    """Analyze a series of games, assuming `player` is the person we care
    about.

    Here we're analyzing the wins and losses for certain openings, to see if
    there are certain openings we're good/bad at.
    """
    # A table of openings. We fill it out to look like:
    # {$OPENING_NAME: {'win: 0, 'loss': 0, 'draw': 0}, ...}
    opening_table = {}
    for game_dict in game_data:
        # Skip any games that don't have opening data.
        # I'm not sure why some games wouldn't have opening data. It's possible
        # lichess hasn't gotten around to analyzing them yet.
        if ignore_game(game_dict):
            continue
        (opening_name, result) = get_game_data(game_dict, player)
        if opening_name not in opening_table:
            opening_table[opening_name] = {
                Result.WIN: 0,
                Result.LOSS: 0,
                Result.DRAW: 0
            }
        opening_table[opening_name][result] += 1
    return opening_table_to_str(opening_table)


def main():
    """Main method."""
    args = util.parse_processor_args()
    game_data = util.read_game_data(args.input_file)
    results = analyze_games(game_data, args.player_name)
    print(results)


if __name__ == "__main__":
    main()
