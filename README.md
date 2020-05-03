# Chess Conducto Pipeline
A pipeline that'll cobble together some data about my lichess games.

## Requirements
Here are the things you need before running:

* Some modern linux installation (Ubuntu 18.04 is nice).
* python3.7 in your $PATH.
* Docker accessible by your current user (`docker run --rm hello-world`
  should run successfully).
* A conducto account. Go here to create one if you haven't yet:
  `https://conducto.com/app/register`.

## How To Run
We use conducto to build our pipelines. The first stage of the pipeline pulls
all the game data. Subsequent stages just analyize the data, so they run in
parallel. All stages print their results to stdout.

To run using canned Lichess data from S3:

```
make pipeline
```

If you've never created a pipeline before, you'll be prompted to enter your
conducto creds. If everything is successful, a browser window should pop up
with the conducto UI and your pipeline ready to execute. To execute your
pipeline, press the "Play" button on the top left. Expand the parallel
`analyze-games` pipeline to see the actual game analysis.

### Run Against Lichess API

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
