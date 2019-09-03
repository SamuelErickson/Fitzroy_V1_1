"""This script should be run once when setting up a Fitzroy box.
This script is responsible for creating data files and configuration files.

Output:
    config.csv saves pin numbers, and things that generally won't change during use,
    but may be specific to a single box in the system
    settings.csv saves temperature/humidity set points, and things that might change
    data_shortterm.csv opens a short term data log that can be accessed by
    data.csv opens a permanent log of all activity just for users in case needed for debugging
"""


import pandas as pd
import numpy as np
import time
import os

# initialize the pippio daemon, which operates the input-output pins
print("starting pigpio daemon")
os.system("sudo pigpiod")

#Edit below dictionary with values to reflect configuration of your equipment
#Pin numbers correspond to BCM numbers - there is more than one way to number

box_config = {'BoxName': ["v2_prototype"],
                'Status':["In Development"],
                'heater_pin': [17],
                'fan_pin': [27],
                 'light_pin': [18],
                 'humidifier_pin': [22],
                'DHT22_pin': [24]
              }

box_settings = {'TempSetPoint': ["TBD"],
                'HumiditySetPoint':["TBD"],
                'LogInterval_sec': [5],
                'DisplayWindow_sec': [86400],
                'LightsOnTime': ["TBD"],
                'LightsOffTime': ["TBD"],
                "Photoperiod (h)":["TBD"],
                "heater_pid_kp":[0.5],
                "heater_pid_kd": [0],
                "heater_pid_ki": [0]
              }

print("This is a prototype version of box V2")
print("Please enter correct values - incorrect values may crash system")

valid_answer = False
while not valid_answer:
    Change_Settings = input("Do you wish to change system settings now? y/n")
    if (Change_Settings == "y" or  Change_Settings == "Y"):
        valid_answer = True
        TempSetPoint = input("Enter temperature setpoint in C (ex: 25)")
        HumiditySetPoint = input("Enter relative humidity setpoint in percentage (ex: 80)")
        LightsOnTime = input("Enter 24h lights on time (ex: 8:30)")
        LightsOffTime = input("Enter lights on time (ex: 20:45)")
    elif (Change_Settings == "n" or Change_Settings == "N"):
        valid_answer = True
        pass
    else:
        print("invalid answer, try again")


valid_answer = False
while not valid_answer:
    Change_PID = input("Do you wish to change control parameters now? y/n")
    if (Change_PID == "y" or Change_PID == "Y"):
        valid_answer = True
        box_settings["heater_pid_kp"] = input("Enter heater_pid_kp (ex: 0.5)")
        box_settings["heater_pid_kd"] = input("Enter heater_pid_kd (ex: 0.5)")
        box_settings["heater_pid_ki"] = input("Enter heater_pid_ki (ex: 0.5)")
    elif (Change_PID == "n" or Change_PID == "N"):
        valid_answer = True
        pass
    else:
        print("invalid answer, try again")







#save





#df_boxconfig = pd.DataFrame(data=box_config)
#df_boxconfig.to_csv("config.csv", index=False)

#df_boxsettings = pd.DataFrame(data=box_settings)
#df_boxsettings.to_csv("settings.csv", index=False)

#df_data_shortterm = pd.DataFrame(columns=["Time", "TemperatureC","TempSetPoint", "Humidity", "HeaterPower", "HumidifierPower", "LightPower"])
#df_data_shortterm.to_csv("data_shortterm.csv", index=False)

#df_data = pd.DataFrame(columns=["Time", "TemperatureC", "Humidity", "HeaterPower", "HumidifierPower", "LightPower"])
#df_data.to_csv("data.csv", index=False)

