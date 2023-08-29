#!/usr/bin/env python3

import sys
import json
from argparse import ArgumentParser

def parse_commandline():
    """Return parsed command args."""

    parser = ArgumentParser(
        prog=sys.argv[0],
        description=(
            "What it does"
            "What it does"
        ),
        epilog=(
            "<end>"
        )
    )
    parser.add_argument(
        'filename',
        help="Input syncfile filepath."
    )
    return parser.parse_args()

if __name__ == "__main__":

    args = parse_commandline()

    with open(args.filename, 'r') as fp:
        parsed = json.load(fp)

    print(
        f'Read sync data from "{args.filename}":\n'
        f"{json.dumps(parsed, indent=3)}"
    )
