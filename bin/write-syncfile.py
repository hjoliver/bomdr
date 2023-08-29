#!/usr/bin/env python3

import sys
import json
import pathlib
import argparse

"""Write a JSON file for a completed workflow sync point.

"""

def parse_commandline():
    """Return parsed command args."""

    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description=(
            "What it does. "
            "What it does"
        ),
        epilog=(
            "<end>"
        )
    )
    parser.add_argument(
        'filename',
        help="Output filename."
    )
    parser.add_argument(
        '-w', '--workflow',
        help="Workflow name.",
        metavar="NAME",
        required=True,
        action='store'
    )
    parser.add_argument(
        '-s', '--sync',
        metavar="Task ID",
        help="(Multiple use.) Record this task's data was succesfully synced.",
        required=True,
        action='append'
    )
    parser.add_argument(
        '-t', '--trigger',
        metavar="Task ID",
        help="(Multiple use.) Trigger this task with children of synced ones.",
        action='append',
    )
    return parser.parse_args()


def main():
    """DOCSTRING

    """
    args = parse_commandline()
    parsed = {
        "workflow": args.workflow,
        "synced": args.sync,
        "trigger": args.trigger
    }

    ofile = pathlib.Path(args.filename)
    print(
        f'Writing sync data to "{ofile}":\n'
        f"{json.dumps(parsed, indent=3)}"
    )

    (ofile.parent).mkdir(parents=True, exist_ok=True)
    with open(ofile, 'w') as fp:
        json.dump(parsed, fp)


if __name__ == "__main__":
    main()
