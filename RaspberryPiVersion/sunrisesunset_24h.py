import pigpio
import numpy as np
from time import sleep  # Importing sleep from time library
from math import sin, pi as piConstant
import sys
import datetime

"""
EIght positional arguments must be passed to this script in the command line
in the correct order

integer light pin
max light duty cycle, float 0-1
integer sunrise/sunset duration in seconds
integer oscillation frequency in hz
integer hour on
integer minute on
integer hour off
integer minute off

Example:
python3 sunrisesunset_24h.py 18 0.75 10 500 8 30 20 45
means drive light with raspberry pi pin 18, maximum duty cycle 0.75, sunrise/sunset duration 10 seconds,
 oscillation frequency 500 hz, on at 8:30 AM, off at 8:45 PM
 
 WITH CURRENT SETTINGS CAN NOT CONTROL MAX LIGHT OUTPUT ALWAYS 100%
"""

checktime_period = 10 #period in seconds between checking time to see whether to proceed

pinNum = int(sys.argv[1])
max_duty_cycle = float(sys.argv[2])
sunriseDuration = int(sys.argv[3])
freq = int(sys.argv[4])
hourOn = int(sys.argv[5])
minOn = int(sys.argv[6])
hourOff = int(sys.argv[7])
minOff = int(sys.argv[8])

n = int(1000000*max_duty_cycle)

timeNow = datetime.datetime.now().time()
timeOn = datetime.time(hourOn, minOn)
timeOff = datetime.time(hourOff, minOff)
isDayTime = (timeNow > timeOn and timeNow<timeOff)


steps = 360 # number of discrete intensity steps
incrementTime = sunriseDuration/(int(max_duty_cycle*steps)+1)


pi = pigpio.pi()
pi.set_mode(pinNum, pigpio.ALT5)
pi.hardware_PWM(pinNum, freq,0)#590000)




try:
    isDayTime = (timeNow > timeOn and timeNow < timeOff)
    while True:        #Sunrise loop
        while not isDayTime: #nighttime loop
            print("Nighttime")
            sleep(checktime_period)
            timeNow = datetime.datetime.now().time()
            isDayTime = (timeNow > timeOn and timeNow<timeOff)
        for i in np.linspace(0,steps,steps+1):
            print(i)
            i = (i/steps/2)*piConstant
            i = int(n*sin(i))
            pi.hardware_PWM(pinNum, freq,i)
            sleep(incrementTime)
        #pi.write(pinNum,1)  #On 100%
        while isDayTime: #daytime loop
            print("Daytime")
            sleep(checktime_period)
            timeNow = datetime.datetime.now().time()
            isDayTime = (timeNow > timeOn and timeNow<timeOff)
        for i in np.linspace(steps,0,steps+1):
            print(i)
            i = (i/steps/2)*piConstant
            i = int(n*sin(i))
            pi.hardware_PWM(pinNum, freq,i)
            sleep(incrementTime)
        #pi.write(pinNum,0)  #On 100%
        #while not isDayTime: #nighttime loop
         #   sleep(checktime_period)
          #  timeNow = datetime.datetime.now().time()
           # isDayTime = (timeNow > timeOn and timeNow<timeOff)
finally: #These lines will execute even if there is an exception error during the sunrise/sunset loops
    # For instance, if the process is killed this should happen
    pi.write(pinNum, 0)
    pi.stop()

