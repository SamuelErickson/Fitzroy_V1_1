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

#Edit below dictionary with values to reflect configuration of your equipment
box_config = {'BoxName': "v2_prototype",
                'Status':"In Development",
                'TempSetPoint': 25,
                'TempLogInterval_sec': 3,
                'TempDisplayWindow_sec': 60*60*24,
                "Photoperiod (h)":"TBD",
                'LightsOnTime': "TBD",
                'LightsOffTime': "TBD",
                'heater_pin': 17,
                'fan_pin': 27,
                 'light_pin': 23,
                 'humidifier_pin': 22,
                    'DHT22_pin': 24
              }

box_settings = {'TempSetPoint': 25,
                'TempLogInterval_sec': 3,
                "Photoperiod (h)":"TBD",
                'LightsOnTime': "TBD",
                'LightsOffTime': "TBD",
              }

#save
df_boxconfig = pd.DataFrame(data=box_config)
df_boxconfig.to_csv("config.csv", index=False)

df_boxsettings = pd.DataFrame(data=box_settings)
df_boxsettings.to_csv("settings.csv", index=False)

df_data_shortterm = pd.DataFrame(columns=["Time", "TemperatureC", "Humidity", "HeaterStatus", "HumidifierStatus", "FanStatus"])
df_data_shortterm.to_csv("data_shortterm.csv", index=False)

df_data = pd.DataFrame(columns=["Time", "TemperatureC", "Humidity", "HeaterStatus", "HumidifierStatus", "FanStatus"])
df_data.to_csv("data.csv", index=False)