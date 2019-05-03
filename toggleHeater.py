import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pinNum = 27
GPIO.setup(pinNum,GPIO.OUT)


if GPIO.input(pinNum) == GPIO.LOW:
     GPIO.output(pinNum, GPIO.HIGH)
     print("heater turned on")
elif GPIO.input(pinNum) == GPIO.HIGH:
     GPIO.output(pinNum, GPIO.LOW)
     print("heater turned off")

else:
    print("error")
