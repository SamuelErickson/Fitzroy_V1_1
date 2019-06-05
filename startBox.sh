#!/usr/bin/env bash

# This shell script runs the commands needed to start one Fitzroy system unit box
# This is the only script that should be modified

# Start a

# initialize the pippio daemon, which operates the input-output pins
sudo pigpiod
screen -d -m -S FitzroyBox bash -c "logTemp_exp7_24hours.py 28"