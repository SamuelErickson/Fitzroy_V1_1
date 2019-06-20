#!/usr/bin/env bash

# If this is the first time running this script, you first need to make it executable by user.

# This shell script runs the commands needed to start one Fitzroy system unit box

# initialize the pippio daemon, which operates the input-output pins
sudo pigpiod

#    Example: python3 run_environmental_control.py 28 80 0.5 8 30 12 00
#    The above command starts a Fitzroy box at 28 C, 80% relative humidity, 50% fan power, with sunrise at 8:30 AM,
#    and a sunset 12 hours 00 minutes later at 20:30.

screen -d -m -S environmental_control bash -c "python3 run_environmental_control.py 28 80 0.5 14 50 1 45"

