"""
Kills all processes, turns off box control systems
"""

import os
import RPi.GPIO as GPIO


os.system("killall screen")

GPIO.cleanup()