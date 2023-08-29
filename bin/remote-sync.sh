#!/usr/bin/env bash

set -eu

REMOTE=$1
FILE=$2  # Path relative to cylc-run.

CYLC_RUN=$HOME/cylc-run

# Replicate source dir structure at target.
TARGET_DIR=$CYLC_RUN/$REMOTE/$(dirname $FILE)
mkdir -p $TARGET_DIR

echo "Copying $FILE to $TARGET_DIR"
cp $CYLC_RUN/$FILE $TARGET_DIR
