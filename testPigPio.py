import pigpio
import numpy as np
from time import sleep  # Importing sleep from time library
from math import sin, pi as piConstant
import sys

if len(sys.argv) >= 4:
    freq = int(sys.argv[3])
elif len(sys.argv) >= 3:
    dayTime = int(sys.argv[2])
elif len(sys.argv) >= 2:
    sunriseDuration = int(sys.argv[1])
else:
    sunriseDuration = 30 #seconds
    dayTime = 0  # seconds
    freq = 500

incrementTime = sunriseDuration/256
pinNum = 21


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
finally:
    print("activated finally")
    pi.write(pinNum, 0)
    pi.stop()
    print("stop")

