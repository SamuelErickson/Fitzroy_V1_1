import RPi.GPIO as GPIO
import pandas as pd
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pinNum = 25
df_config = pd.read_csv('../config.csv')
pinNum = int(df_config["humidifier_pin"].iloc[0])
GPIO.setup(pinNum,GPIO.OUT)




if GPIO.input(pinNum) == GPIO.LOW:
     GPIO.output(pinNum, GPIO.HIGH)
     print("humidifier turned on")
elif GPIO.input(pinNum) == GPIO.HIGH:
     GPIO.output(pinNum, GPIO.LOW)
     print("humidifier turned off")

else:
    print("error")
