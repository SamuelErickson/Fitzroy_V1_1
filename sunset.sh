#!/usr/bin/env bash

# open a screen window called led_control
# send a SIGINT signal, equivalent to ctrl+C
# shuts down any python script running in that window
screen -S led_control -X stuff ^C