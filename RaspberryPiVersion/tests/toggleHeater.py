import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pinNum = 27
df_config = pd.read_csv('config.csv')
pinNum = int(df_config["heater_pin"].iloc[0])
GPIO.setup(pinNum,GPIO.OUT)

import pandas as pd



if GPIO.input(pinNum) == GPIO.LOW:
     GPIO.output(pinNum, GPIO.HIGH)
     print("heater turned on")
elif GPIO.input(pinNum) == GPIO.HIGH:
     GPIO.output(pinNum, GPIO.LOW)
     print("heater turned off")

else:
    print("error")
