# Chess Conducto Pipeline
A pipeline that'll cobble together some data about my lichess games.

## How To Run
We use conducto to build our pipelines. The first stage of the pipeline pulls
all the game data. Subsequent stages just analyize the data, so they run in
parallel. All stages print their results to stdout.

To run using canned Lichess data from S3:

```
make pipeline
```

If successful, a browser window should pop up with the conducto UI and your
pipeline ready to execute. To execute your pipeline, press the "Play" button on
the top left.. Expand the parallel `analyze-games` pipeline to see the actual
game analysis.


Alternatively you can run pulling the newest data directly from lichess:

```
make pipeline-fresh
```

NB: If you want to pull fresh from lichess, you'll need to generate a lichess
API token and save it as a secret in your conducto account called
`LICHESS_TOKEN`.

## Python venv
I use the venv python module to make venvs. On ubuntu there are sometimes weird
issues where python complains that the `ensurepip` library is missing.  You can
run `apt install python3.7-venv` to install that missing lib.

## Lichess API
Here's the lichess API doc: https://berserk.readthedocs.io/en/master/usage.html

It's pretty easy to use, and only requires an API token. You can generate an
API token at https://lichess.org/account/oauth/token.
