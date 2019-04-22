import pigpio
from time import sleep  # Importing sleep from time library

pinNum = 21

pi = pigpio.pi()
pi.set_mode(pinNum,pigpio.OUTPUT)
pi.write(pinNum,1)
sleep(2)
pi.write(pinNum,0)
sleep(1)
pi.set_PWM_dutycycle(pinNum,   192) # PWM off
sleep(1)
pi.set_PWM_dutycycle(pinNum,   128) # PWM off
sleep(1)
pi.set_PWM_dutycycle(pinNum,   64) # PWM off

pi.stop()