#!/usr/bin/env bash

# opens a new screen called led_control, detaches from screen window
# and then runs sunrise_gpio.py script in the new window

screen -d -m -S newScreen bash -c "python3 sunrisesunset_demo.py"