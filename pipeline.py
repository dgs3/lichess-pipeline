#!/usr/bin/env python3.7
"""
A pipeline to analyze Dave's lichess games.
"""

import conducto

GAMES_DATA_FILE = 'games.json'
PLAYER_NAME = 'dgs3'

PIPELINE_IMG = conducto.Image("python:3.7", copy_dir=".")


def get_lichess_token() -> str:
    """Get the lichess token from my account's secrets."""
    token = conducto.api.Auth().get_token_from_shell()
    api = conducto.api.Secrets()
    secrets = api.get_user_secrets(token)
    return secrets['LICHESS_TOKEN']


def download_games() -> conducto.Exec:
    """Executor to Download lichess games."""
    token = get_lichess_token()
    args = [
        'venv/bin/python3.7',
        'scripts/download_lichess_data.py',
        f'--player-name={PLAYER_NAME}',
        f'--output-file={GAMES_DATA_FILE}',
        f'--token={token}',
    ]
    cmd = ' '.join(args)
    return conducto.Exec(cmd)


def openings_win_loss_rate() -> conducto.Exec:
    """Executor to analyze openings from lichess data."""
    args = [
        'venv/bin/python3.7',
        'scripts/openings_win_rate.py',
        f'--input-file={GAMES_DATA_FILE}',
        f'--player-name={PLAYER_NAME}',
    ]
    cmd = ' '.join(args)
    return conducto.Exec(cmd)


def lichess() -> conducto.Exec:
    """Executor for the lichess pipeline.

    This pipeline pulls all of my lichess games and sees how I can improve.
    """
    with conducto.Serial(doc=conducto.util.magic_doc(),
                         image=PIPELINE_IMG) as pipeline:
        pipeline['download-from-lichess'] = download_games()
        with conducto.Parallel(name='analyze-games') as analyze_pipeline:
            analyze_pipeline[
                'openings-win-loss-rate'] = openings_win_loss_rate()
    return pipeline


if __name__ == "__main__":
    conducto.main(default=lichess)
