"""A util package for some scripts."""

import argparse
import json


def parse_processor_args(description) -> argparse.Namespace:
    """Common args for game data processor scripts."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--input-file',
                        help='Games file to analyze.',
                        required=True)
    parser.add_argument('--player-name',
                        help='Lichess player name to analyze.',
                        required=True)
    return parser.parse_args()


def read_game_data(filepath) -> list:
    """Read in and parse a game file.

    The game file is expected to be a json formatted list.
    """
    with open(filepath) as fil:
        return json.load(fil)


def game_has_opening_data(game_dict) -> bool:
    """Returns True if this game has opening data. False otherwise."""
    return 'opening' in game_dict


def get_game_winner(game_dict) -> str:
    """Returns the name of the game winner."""
    # Here the value of winner is the color that won (i.e. white, black)
    winner_color = game_dict['winner']
    return game_dict['players'][winner_color]['user']['name']


def get_opening_name(game_dict) -> str:
    """Gets the name of the opening used."""
    return game_dict['opening']['name']
