#!/usr/bin/env python3.7
"""
A pipeline to analyze Dave's lichess games.
"""

import conducto

GAMES_DATA_FILE = 'games.json'
PLAYER_NAME = 'dgs3'


def env_vars() -> conducto.Exec:
    """Executor to get some env vars to supply to the conducto pipeline.

    Mostly used to contain the lichess API token.
    """
    cmd = 'env | grep -e LICHESS_TOKEN'
    return conducto.Exec(cmd, doc=conducto.util.magic_doc(), name='env-vars')


def download_games() -> conducto.Exec:
    """Executor to Download lichess games."""
    args = [
        'python3.7',
        'scripts/download_lichess_data.py',
        f'--player-name={PLAYER_NAME}',
        f'--output-file={GAMES_DATA_FILE}',
    ]
    cmd = ' '.join(args)
    return conducto.Exec(cmd, name='download-from-lichess')


def openings_win_loss_rate() -> conducto.Exec:
    """Executor to analyze openings from lichess data."""
    args = [
        'python3.7',
        'scripts/openings_win_rate.py',
        f'--input-file={GAMES_DATA_FILE}',
        f'--player-name={PLAYER_NAME}',
    ]
    cmd = ' '.join(args)
    return conducto.Exec(cmd, name='openings_win_loss_rate')


def lichess() -> conducto.Exec:
    """A data pipeline to pull all of my lichess games and see what openings
    I need to work on, if I equalize out of openings, etc.
    """
    with conducto.Serial(doc=conducto.util.magic_doc()) as pipeline:
        pipeline['env-vars'] = env_vars()
        pipeline['download-from-lichess'] = download_games()
        with conducto.Parallel(name='analyze-games') as analyze_pipeline:
            analyze_pipeline[
                'openings-win-loss-rate'] = openings_win_loss_rate()
    return pipeline


if __name__ == "__main__":
    conducto.main(default=lichess)
