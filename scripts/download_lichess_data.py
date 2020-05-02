#!/usr/bin/env python3.7
"""
Script used to download lichess game data.
"""

import argparse
import datetime
import json
import os

import berserk


def parse_args() -> argparse.Namespace:
    """Parse some args."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--player-name',
                        help='Lichess player name to analyze.',
                        required=True)
    parser.add_argument('--token', help='Lichess API token.')
    parser.add_argument('--output-file',
                        help='File to output game data to.',
                        required=True)
    return parser.parse_args()


class LichessEncoder(json.JSONEncoder):
    """A decoder for lichess game data.

    Lichess game data uses datetime objects, which aren't serializable. We
    serialize them as timestamps.
    """

    # Unfortunately super().default uses `o`, and not something more
    # comprehensible like `obj`. Not using `o` gives pylint errors. :(
    def default(self, o) -> str:
        """Default Encoder function.

        :param obj: Object to encode.
        :returns: JSON encoded object.
        """
        if isinstance(o, datetime.datetime):
            return self.serialize_datetime_obj(o)
        return super().default(o)

    @staticmethod
    def serialize_datetime_obj(obj) -> str:
        """Serialize a datetime object for json.

        Here a serialized datetime object is just the isoformat string.
        """
        return obj.isoformat()


def get_token_from_env() -> str:
    """Gets a lichess token from the env."""
    return os.environ['LICHESS_TOKEN']


def main():
    """Main method."""
    args = parse_args()
    token = args.token
    # Having the token in the env supports conducto a bit better.
    if args.token is None:
        token = get_token_from_env()
    session = berserk.TokenSession(token)
    client = berserk.Client(session=session)
    games = client.games.export_by_player(args.player_name)
    full_game_data = []
    for game in games:
        full_game_data.append(client.games.export(game['id']))
    with open(args.output_file, 'w') as fil:
        json.dump(full_game_data, fil, cls=LichessEncoder)


if __name__ == "__main__":
    main()
