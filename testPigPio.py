import pigpio
import numpy as np
from time import sleep  # Importing sleep from time library
from math import pi as piConstant
from math import sin

sunriseDuration = 30 #seconds
incrementTime = sunriseDuration/256
dayTime = 0 #seconds
freq = 500

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
    #i = int(i)
    #pi.set_PWM_dutycycle(pinNum, 0)  # PWM off
   # sleep(incrementTime)



#pi.set_PWM_dutycycle(pinNum,   192) # PWM off
#sleep(1)
#pi.set_PWM_dutycycle(pinNum,   128) # PWM off
#sleep(1)
#pi.set_PWM_dutycycle(pinNum,   64) # PWM off

#pi.write(pinNum,0)
