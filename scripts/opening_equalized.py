#!/usr/bin/env python3.7
"""
Script used to determine if I was able to equalize, win or lose out of the
opening.

I say I equalized if the eval is -100 <= EVAL <= 100.

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
    """An enum to hold some data about opening results."""
    WIN = 'win'
    LOSS = 'loss'
    EQUAL = 'equal'


class Color(enum.Enum):
    """An enum to hold piece color."""
    WHITE = 'white'
    BLACK = 'black'


def get_opening_eval(game_data) -> int:
    """Get the eval after an opening is "done".

    It's kind of hard to generalize how many moves it takes to finish an
    opening. I'm going to just say after the players have gone through 8
    turns, the opening is done.
    """
    analysis = game_data['analysis']
    # 8 rounds means 16 individual moves.
    limit = 16
    if len(analysis) < limit:
        final_eval = analysis[-1]
    else:
        # Use `limit-1` because the first move is move 0
        final_eval = analysis[limit - 1]
    return final_eval['eval']


def get_player_color(game_data, player) -> Color:
    """Gets the color `player` played as."""
    if game_data['players'][Color.WHITE.value]['user']['name'] == player:
        return Color.WHITE
    return Color.BLACK


def get_game_data(game_dict, player) -> tuple:
    """Gets some data about whether or not I was able to equalize out of this
    opening."""
    opening_name = util.get_opening_name(game_dict)
    opening_eval = get_opening_eval(game_dict)
    player_color = get_player_color(game_dict, player)
    # An eval of 100 means white has a clear edge out of the opening.
    if opening_eval > 100:
        if player_color == Color.WHITE:
            status = Result.WIN
        else:
            status = Result.LOSS
    # An eval of -100 means black probably won the opening.
    elif opening_eval < -100:
        if player_color == Color.BLACK:
            status = Result.WIN
        else:
            status = Result.LOSS
    else:
        status = Result.EQUAL
    return (opening_name, status)


def game_has_eval_data(game_dict) -> bool:
    """Returns True if this game has eval data. False otherwise."""
    return 'analysis' in game_dict


def ignore_game(game_dict) -> bool:
    """Returns True if we should just ignore this game data. False otherwise.

    We ignore some games if they have insufficient date.
    """
    return not util.game_has_opening_data(game_dict) or not game_has_eval_data(
        game_dict)


def equalize_table_to_str(equalize_table) -> str:
    """Format an equalize table to string for printing."""
    to_return = ""
    for opening_name, data in equalize_table.items():
        to_add = [
            f'{opening_name}:\n',
            f'    Wins: {data[Result.WIN]}\n',
            f'    Losses: {data[Result.LOSS]}\n',
            f'    Equalizes: {data[Result.EQUAL]}\n',
        ]
        to_return += ' '.join(to_add)
    return to_return


def analyze_games(game_data, player) -> str:
    """Analyze a series of games, determining if I was able to win, lose, or
    equalize out of the opening.
    """
    equalize_table = {}
    for game_dict in game_data:
        if ignore_game(game_dict):
            continue
        (opening_name, status) = get_game_data(game_dict, player)
        if opening_name not in equalize_table:
            equalize_table[opening_name] = {
                Result.WIN: 0,
                Result.LOSS: 0,
                Result.EQUAL: 0
            }
        equalize_table[opening_name][status] += 1
    return equalize_table_to_str(equalize_table)


def main():
    """Main method."""
    args = util.parse_processor_args(__doc__)
    game_data = util.read_game_data(args.input_file)
    results = analyze_games(game_data, args.player_name)
    print(results)


if __name__ == "__main__":
    main()
