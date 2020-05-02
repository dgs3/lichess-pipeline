#!/usr/bin/env python3.7
"""
A pipeline to analyze Dave's lichess games.
"""

import conducto


def hello() -> conducto.Exec:
    """A hello pipeline."""
    return conducto.Exec("echo This is some stuff.",
                         image="bash:5.0",
                         doc=__doc__)


if __name__ == "__main__":
    conducto.main(default=hello)
