#!/usr/bin/env bash

# This shell script runs the commands needed to start one Fitzroy system unit box
# This is the only script that should be modified

# Start a

# initialize the pippio daemon, which operates the input-output pins
sudo pigpiod
screen -d -m -S FitzroyBox bash -c "python3 sunrisesunset_demo.py 1 1 500"