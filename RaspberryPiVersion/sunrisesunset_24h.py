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
python3 sunrisesunset_24h.py 23 0.75 10 500 8 30 20 45
means drive light with raspberry pi pin 23, maximum duty cycle 0.75, sunrise/sunset duration 10 seconds,
 oscillation frequency 500 hz, on at 8:30 AM, off at 8:45 PM
"""

#
#sunriseDuration = 10
#freq = 500
#max_duty_cycle = 0.5

checktime_period = 10 #period in seconds between checking time to see whether to proceed

pinNum = int(sys.argv[1])
max_duty_cycle = int(sys.argv[2])
sunriseDuration = int(sys.argv[3])
freq = int(sys.argv[4])
hourOn = int(sys.argv[5])
minOn = int(sys.argv[6])
hourOff = int(sys.argv[7])
minOff = int(sys.argv[8])


timeNow = datetime.datetime.now().time()
timeOn = datetime.time(hourOn, minOn)
timeOff = datetime.time(hourOff, minOff)
isDayTime = (timeNow > timeOn and timeNow<timeOff)

incrementTime = sunriseDuration/256



pi = pigpio.pi()
pi.set_PWM_frequency(pinNum,freq)
pi.set_mode(pinNum,pigpio.OUTPUT)
pi.write(pinNum,0)

n = 256
try:
    while True:        #Sunrise loop
        for i in np.linspace(0,int(max_duty_cycle)*255,int(max_duty_cycle)*255+1):
            i = (i/n/2)*piConstant
            i = int(n*sin(i))
            pi.set_PWM_dutycycle(pinNum, i)  # PWM off
            sleep(incrementTime)
        while isDayTime: #daytime loop
            sleep(checktime_period)
            timeNow = datetime.datetime.now().time()
            isDayTime = (timeNow > timeOn and timeNow<timeOff)
        for i in np.linspace(int(max_duty_cycle)*255,0,int(max_duty_cycle)*255+1): #sunset loop
            i = (i/n) * piConstant/2
            i = int(n * sin(i))
            pi.set_PWM_dutycycle(pinNum, i)  # PWM off
            sleep(incrementTime)
        while not isDayTime: #nighttime loop
            sleep(checktime_period)
            timeNow = datetime.datetime.now().time()
            isDayTime = (timeNow > timeOn and timeNow<timeOff)
finally: #These lines will execute even if there is an exception error during the sunrise/sunset loops
    # For instance, if the process is killed this should happen
    pi.write(pinNum, 0)
    pi.stop()

