#!/usr/bin/env bash

# This shell script runs the commands needed to start one Fitzroy system unit box
# This is the only script that should be modified

# Start a
screen -d -m -S FitzroyBox bash -c "python3 sunrise.py"