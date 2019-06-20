import pigpio
import numpy as np
from time import sleep  # Importing sleep from time library
from math import sin, pi as piConstant
import sys
import datetime

"""
Three optional arguments can be passed to this script in the command line
1: hour on
2: minute on
3: hour off
4: minute off
Example:
python3 scriptName.py 8 30 20 45
means on at 8:30 AM, off at 8:45 PM
"""

#
sunriseDuration = 10
freq = 500

hourOn = int(sys.argv[1])
minOn = int(sys.argv[2])
hourOff = int(sys.argv[3])
minOff = int(sys.argv[4])

timeNow = datetime.datetime.now().time()
timeOn = datetime.time(hourOn, minOn)
timeOff = datetime.time(hourOff, minOff)
isDayTime = (timeNow > timeOn and timeNow<timeOff)

incrementTime = sunriseDuration/256
pinNum = 23


pi = pigpio.pi()
pi.set_PWM_frequency(pinNum,freq)
pi.set_mode(pinNum,pigpio.OUTPUT)
pi.write(pinNum,0)

n = 256
try:
    while True:
        for i in np.linspace(0,255,256):
            i = (i/n/2)*piConstant
            i = int(n*sin(i))
            pi.set_PWM_dutycycle(pinNum, i)  # PWM off
            sleep(incrementTime)
        while isDayTime:
            sleep(15)
            timeNow = datetime.datetime.now().time()
            isDayTime = (timeNow > timeOn and timeNow<timeOff)
        for i in np.linspace(255,0,256):
            i = (i/n) * piConstant/2
            i = int(n * sin(i))
            pi.set_PWM_dutycycle(pinNum, i)  # PWM off
            sleep(incrementTime)
        while not isDayTime:
            sleep(5000)
            timeNow = datetime.datetime.now().time()
            isDayTime = (timeNow > timeOn and timeNow<timeOff)
finally: #These lines will execute even if there is an exception error during the sunrise/sunset loops
    pi.write(pinNum, 0)
    pi.stop()

