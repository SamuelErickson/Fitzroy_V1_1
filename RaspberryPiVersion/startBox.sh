#!/usr/bin/env bash

# This shell script runs the commands needed to start one Fitzroy system unit box
# This is the only script that should be modified

# Start a

# initialize the pippio daemon, which operates the input-output pins
sudo pigpiod

#
screen -d -m -S environmental_control bash -c "python3 run_environmental_control.py 28 80 0.5 8 30 12 00 23 0.75 10 500 14 31 0 1
"