# Chess Conducto Pipeline
A pipeline that'll cobble together some data about my lichess games.

## Python venv
I use the venv python module to make venvs. On ubuntu there are sometimes
weird issues where python complains that the `ensurepip` library is missing.
You can run `apt install python3.7-venv` to install that missing lib.

## Lichess API
Here's the lichess API doc: https://berserk.readthedocs.io/en/master/usage.html

It's pretty easy to use, and only requires an API token. You can generate an
API token at https://lichess.org/account/oauth/token.
