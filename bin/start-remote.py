#!/usr/bin/env python3

import os
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


def start_from_syncpoint(parsed):
    """DOC"""
    command = (
        f"rm -r {os.environ['HOME']}/cylc-run/REMOTE/"
        f"{parsed['workflow']}/.service"
    )
    os.system(command)

    command = f"cylc play REMOTE/{parsed['workflow']}"
    for task in parsed["synced"] + parsed["trigger"]:
        command += f" --start-task={task}"
    os.system(command)

    for task in parsed["synced"]:
        command = f"cylc set-outputs --flow=1 REMOTE/{parsed['workflow']}//{task}"
        os.system(command)

    for task in parsed["synced"]:
        command = f"cylc remove REMOTE/{parsed['workflow']}//{task}"
        os.system(command)


if __name__ == "__main__":

    args = parse_commandline()

    with open(args.filename, 'r') as fp:
        parsed = json.load(fp)

    print(f"{json.dumps(parsed, indent=3)}")
    start_from_syncpoint(parsed)
