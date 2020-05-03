#!/usr/bin/env python3.7
"""
A pipeline to analyze Dave Sayles' lichess games.
"""

import conducto

GAMES_DATA_FILE = 'games.json'
PLAYER_NAME = 'dgs3'

VENV_PYTHON = 'venv/bin/python3.7'

PIPELINE_IMG = conducto.Image(dockerfile='Dockerfile')


def get_lichess_token() -> str:
    """Get the lichess token from my account's secrets."""
    token = conducto.api.Auth().get_token_from_shell()
    api = conducto.api.Secrets()
    secrets = api.get_user_secrets(token)
    return secrets['LICHESS_TOKEN']


def download_games_from_s3() -> conducto.Exec:
    """Executor to download canned games from s3."""
    games_url = 'https://sayles-lichess-games.s3.amazonaws.com/games.zip'
    args = [
        f'curl --output - {games_url}',
        '|',
        # We assume `zcat` is readily available in PIPELINE_IMG.
        'zcat',
        '>',
        GAMES_DATA_FILE,
    ]
    cmd = ' '.join(args)
    return conducto.Exec(cmd)


def download_games_from_lichess() -> conducto.Exec:
    """Executor to download games directly from lichess."""
    token = get_lichess_token()
    args = [
        VENV_PYTHON,
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
        VENV_PYTHON,
        'scripts/openings_win_rate.py',
        f'--input-file={GAMES_DATA_FILE}',
        f'--player-name={PLAYER_NAME}',
    ]
    cmd = ' '.join(args)
    return conducto.Exec(cmd)


def opening_equalized() -> conducto.Exec:
    """Executor to analyze if any player has an edge during the opening."""
    args = [
        VENV_PYTHON,
        'scripts/opening_equalized.py',
        f'--input-file={GAMES_DATA_FILE}',
        f'--player-name={PLAYER_NAME}',
    ]
    cmd = ' '.join(args)
    return conducto.Exec(cmd)


def add_analyzers():
    """Adds some analyzers to a pipeline.

    Expected to be used in the `with` context of a parent pipeline.
    """
    with conducto.Parallel(name='analyze-games') as analyze_pipeline:
        analyze_pipeline['openings-win-loss-rate'] = openings_win_loss_rate()
        analyze_pipeline['opening-equalized'] = opening_equalized()


def lichess_canned() -> conducto.Exec:
    """Executor for the lichess pipeline.

    This'll pull down a zipfile of canned lichess data, so no api token is
    required.
    """
    with conducto.Serial(doc=conducto.util.magic_doc(),
                         image=PIPELINE_IMG) as pipeline:
        pipeline['download-from-s3'] = download_games_from_s3()
        add_analyzers()
    return pipeline


def lichess_fresh() -> conducto.Exec:
    """Executor for the lichess pipeline.

    This'll pull down data fresh from lichess, so a conducto secret called
    LICHESS_TOKEN is necessary. The token can be generated at:
    `https://lichess.org/account/oauth/token`.
    """
    with conducto.Serial(doc=conducto.util.magic_doc(),
                         image=PIPELINE_IMG) as pipeline:
        pipeline['download-from-lichess'] = download_games_from_lichess()
        add_analyzers()
    return pipeline


if __name__ == "__main__":
    conducto.main(default=lichess_canned)
