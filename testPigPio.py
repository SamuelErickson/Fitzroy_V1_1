import pigpio
import numpy as np
from time import sleep  # Importing sleep from time library

pinNum = 21

pi = pigpio.pi()
pi.set_mode(pinNum,pigpio.OUTPUT)
pi.write(pinNum,0)

for i in np.linspace(0,255,256):
    i = int(i)
    pi.set_PWM_dutycycle(pinNum, i)  # PWM off
    sleep(0.1)
pi.write(pinNum,0)

#pi.set_PWM_dutycycle(pinNum,   192) # PWM off
#sleep(1)
#pi.set_PWM_dutycycle(pinNum,   128) # PWM off
#sleep(1)
#pi.set_PWM_dutycycle(pinNum,   64) # PWM off

#pi.write(pinNum,0)
pi.stop()