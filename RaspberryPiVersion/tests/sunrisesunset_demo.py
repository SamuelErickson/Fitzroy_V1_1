import pigpio
import numpy as np
from time import sleep  # Importing sleep from time library
from math import sin, pi as piConstant
import sys

"""
Three optional arguments can be passed to this script in the command line
1: sunriseDuration in seconds
2: daytime in seconds
3: frequency in hertz
Example:
python3 scriptName.py 20 5 300
"""

#
if len(sys.argv) >= 4:
    freq = int(sys.argv[3])
    dayTime = int(sys.argv[2])
    sunriseDuration = int(sys.argv[1])
elif len(sys.argv) >= 3:
    freq = 500
    dayTime = int(sys.argv[2])
    sunriseDuration = int(sys.argv[1])
elif len(sys.argv) >= 2:
    dayTime = 0  # seconds
    freq = 500
    sunriseDuration = int(sys.argv[1])
else:
    sunriseDuration = 30 #seconds
    dayTime = 0  # seconds
    freq = 500

incrementTime = sunriseDuration/256
pinNum = 23


pi = pigpio.pi()
pi.set_PWM_frequency(pinNum,freq)
pi.set_mode(pinNum,pigpio.OUTPUT)
pi.write(pinNum,0)

n = 256
try:
    for i in np.linspace(0,255,256):
        i = (i/n/2)*piConstant
        i = int(n*sin(i))
        pi.set_PWM_dutycycle(pinNum, i)  # PWM off
        sleep(incrementTime)
    sleep(dayTime)
    for i in np.linspace(255,0,256):
        i = (i/n) * piConstant/2
        i = int(n * sin(i))
        pi.set_PWM_dutycycle(pinNum, i)  # PWM off
        sleep(incrementTime)
finally: #These lines will execute even if there is an exception error during the sunrise/sunset loops
    pi.write(pinNum, 0)
    pi.stop()

