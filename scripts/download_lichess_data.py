#!/usr/bin/env python3.7

"""
Script used to download lichess game data.
"""

import argparse
import datetime
import json

import berserk

def parse_args():
    """Parse some args.

    :returns: args domain object.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--player-name',
                        help='Lichess player name to analyze.')
    parser.add_argument('--token',
                        help='Lichess API token.')
    parser.add_argument('--output-file',
                        help='File to output game data to.')
    return parser.parse_args()

class LichessEncoder(json.JSONEncoder):
    """A decoder for lichess game data.

    Lichess game data uses datetime objects, which aren't serializable. We
    serialize them as timestamps.
    """

    def default(self, obj):
        """Default Encoder function.

        :param obj: Object to encode.
        :returns: JSON encoded object.
        """
        if isinstance(obj, datetime.datetime):
            return self.serialize_datetime_obj(obj)
        else:
            return json.JSONEncoder.default(self, obj)

    @staticmethod
    def serialize_datetime_obj(obj):
        """Serialize a datetime object for json.

        Here a serialized datetime object is just the isoformat string.
        """
        return obj.isoformat()

def main():
    """Main method."""
    args = parse_args()
    session = berserk.TokenSession(args.token)
    client = berserk.Client(session=session)
    games = client.games.export_by_player(args.player_name)
    # Games comes in as a generator
    games_list = list(games)
    with open(args.output_file, 'w') as fil:
        json.dump(games_list, fil, cls=LichessEncoder)

if __name__ == "__main__":
    main()
