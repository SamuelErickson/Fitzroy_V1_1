import pigpio
from time import sleep  # Importing sleep from time library

pinNum = 21

pi = pigpio.pi()
pi.set_mode(21,pigpio.OUTPUT)
pi.write(pinNum,1)
sleep(2)
pi.write(pinNum,0)
sleep(2)
pi.stop()