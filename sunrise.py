
""" Turn on light with PWM
"""


import RPi.GPIO as GPIO  # Importing RPi library to use the GPIO pins
from time import sleep  # Importing sleep from time library


max_duty_cycle = 100 #final percent duty cycle 0 < dc < 100
sunrise_period = 30 #seconds
steptime = sunrise_period/max_duty_cycle #time between steps in sunrise/sunset


#Set pins
led_pin = 21  # Initializing the GPIO pin 21 for LED
GPIO.setmode(GPIO.BCM)  # We are using the BCM pin numbering
GPIO.setwarnings(False)
GPIO.setup(led_pin, GPIO.OUT)  # Declaring pin 21 as output pin
pwm = GPIO.PWM(led_pin, 100)  # Created a PWM object with frequency of 100 hz
pwm.start(0)  # Started PWM at 0% duty cycle
try:
    for x in range(max_duty_cycle):
        pwm.ChangeDutyCycle(x)  # Change duty cycle
        sleep(steptime)  # Delay of 10mS
    while True:
        sleep(1)
except KeyboardInterrupt:
    for x in range(max_duty_cycle, 0, -1):
        pwm.ChangeDutyCycle(x)  # Change duty cycle
        sleep(steptime) #int(10/n))  # Delay of 10mS
finally:
    pwm.stop()  # Stop the PWM
    GPIO.cleanup()  # Make all the output pins LOW


