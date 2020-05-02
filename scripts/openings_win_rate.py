#!/usr/bin/env python3.7
"""Module to determine the win/loss rate of certain openings."""

import argparse
import enum
import json


class Result(enum.Enum):
    """Enum to hold game results."""
    WIN = 'win'
    LOSS = 'loss'
    DRAW = 'draw'
    # I'm not sure what the difference between these is. Could be lichess isn't
    # very strict with the results field.
    TIMEOUT = 'timeout'
    OUT_OF_TIME = 'outoftime'


def parse_args() -> argparse.Namespace:
    """Parse some args."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-file',
                        help='Games file to analyze.',
                        required=True)
    parser.add_argument('--player-name',
                        help='Lichess player name to analyze.',
                        required=True)
    return parser.parse_args()


def get_game_data(game_dict, player) -> dict:
    """Parses some game data from a lichess game dict."""
    opening_name = game_dict['opening']['name']
    if game_dict['status'] == Result.DRAW.value:
        return (opening_name, Result.DRAW)
    # The winner is the color that won (i.e. white, black)
    winner = game_dict['winner']
    winner_name = game_dict['players'][winner]['user']['name']
    return (opening_name, Result.WIN if winner_name == player else Result.LOSS)


def game_has_opening_data(game_dict) -> bool:
    """Returns True if this game has opening data. False otherwise."""
    return 'opening' in game_dict


def game_is_timeout(game_dict) -> bool:
    """Returns True if this game is a timeout. False otherwise.

    For some reason lichess doesn't keep winner data on timeout games.
    :shrug:.
    """
    return game_dict['status'] in [
        Result.TIMEOUT.value, Result.OUT_OF_TIME.value
    ]


def opening_table_to_markdown(game_data) -> str:
    """Format an opening table to markdown."""
    markdown = "<ConductoMarkdown>"
    markdown += "<table><thead><tr>"
    markdown += "<th>Opening Name</th>"
    markdown += "<th>Wins</th>"
    markdown += "<th>Losses</th>"
    markdown += "<th>Draws</th>"
    markdown += "</tr></thead>"
    markdown += "<tbody>"
    for opening_name, data in game_data.items():
        markdown += "<tr>"
        markdown += f"<td>{opening_name}</td>"
        markdown += f"<td>{data[Result.WIN]}</td>"
        markdown += f"<td>{data[Result.LOSS]}</td>"
        markdown += f"<td>{data[Result.DRAW]}</td>"
    markdown += "</tbody>"
    markdown += "/table"
    markdown += "</ConductoMarkdown>"
    return markdown


def analyze_games(game_data, player) -> str:
    """Analyze a series of games, assuming `player` is the person we care
    about.

    Here we're analyzing the wins and losses for certain openings, to see if
    there are certain openings we're good/bad at.
    """
    # A table of openings. We fill it out to look like:
    # {$OPENING_NAME: {'win: 0, 'loss': 0, 'draw': 0}, ...}
    opening_table = {}
    for game in game_data:
        # Skip any games that don't have opening data.
        # I'm not sure why some games wouldn't have opening data. It's possible
        # lichess hasn't gotten around to analyzing them yet.
        if not game_has_opening_data(game) or game_is_timeout(game):
            continue
        (opening_name, result) = get_game_data(game, player)
        if opening_name not in opening_table:
            opening_table[opening_name] = {
                Result.WIN: 0,
                Result.LOSS: 0,
                Result.DRAW: 0
            }
        opening_table[opening_name][result] += 1
    return opening_table_to_markdown(opening_table)


def main():
    """Main method."""
    args = parse_args()
    with open(args.input_file) as fil:
        game_data = json.load(fil)
    results = analyze_games(game_data, args.player_name)
    print(results)


if __name__ == "__main__":
    main()
