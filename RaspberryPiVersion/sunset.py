import pigpio
import numpy as np
from time import sleep  # Importing sleep from time library
from math import sin, pi as piConstant
import sys
import datetime

"""
Do sunrise, then leave light on

EIght positional arguments must be passed to this script in the command line
in the correct order

integer light pin
max light duty cycle, float 0-1
integer sunrise/sunset duration in seconds
integer oscillation frequency in hz


Example:
python3 sunrisesunset_24h.py 18 0.75 10 500
means drive light with raspberry pi pin 18, maximum duty cycle 0.75, sunrise/sunset duration 10 seconds,
 oscillation frequency 500 hz, on at 8:30 AM, off at 8:45 PM
"""

checktime_period = 3 #period in seconds between checking time to see whether to proceed

pinNum = int(sys.argv[1])
max_duty_cycle = float(sys.argv[2])
sunriseDuration = int(sys.argv[3])
freq = int(sys.argv[4])

n = int(1000000*max_duty_cycle)

steps = 100 # number of discrete intensity steps
incrementTime = sunriseDuration/(int(max_duty_cycle*steps)+1)

pi = pigpio.pi()
pi.set_mode(pinNum, pigpio.ALT5)
for i in np.linspace(steps,0,steps+1):
    print(i)
    i = (i/steps/2)*piConstant
    i = int(n*sin(i))
    pi.hardware_PWM(pinNum, freq,i)
    sleep(incrementTime)
pi.stop()

