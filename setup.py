import pandas as pd
import numpy as np
import time

# Write a csv file containing tank names, sensors, etc

#Edit below dictionary with values to reflect configuration of your equipment
BoxConfig = {'BoxName': ["Box_1"],
                'Status':["In Development"],
                'TempSetPoint': [25],
                'TempLogInterval_sec': [3],
                'TempDisplayWindow_sec': [60*60*24],
                "Photoperiod (h)":["TBD"],
                'LightsOnTime': ["TBD"],
                'LightsOffTime': ["TBD"],
                'heater_pin': [4],
                'fan_pin': [17],
                 'light_pin': ["TBD"],
                 'humidifier_pin': ["TBD"],
                    'DHT22_pin': ["TBD"]
             }
# 24 hours display in short term data right now

#Function: Initialize lights!
timeNow = time.asctime()
#CHECK whether light should be on right now or off right now and set up lights...

df_BoxConfig = pd.DataFrame(data=BoxConfig)
df_BoxConfig.to_csv("config.csv",index=False)

df_TempData_shortTerm = pd.DataFrame(columns=["Time","TemperatureC","Humidity","HeaterStatus","HumidifierStatus","FanStatus"])
df_TempData_shortTerm.to_csv("tempData_shortTerm.csv",index=False)

df_TempData = pd.DataFrame(columns=["Time","TemperatureC","Humidity","HeaterStatus","HumidifierStatus","FanStatus"])
df_TempData.to_csv("tempData.csv",index=False)

print(df_BoxConfig)
print(df_TempData)




#df_TankStatus = pd.DataFrame(columns=TankConfig["TankName"],index=["Temp","LightStatus"])


#Start some tanks right away, need to check time first
#tanks = ['Tank_A1', 'Tank_A2']
#df_TankStatus.loc["LightStatus", tanks] = 'ON'



#df_Thermo1 = pd.DataFrame(columns=["Time","Temp"])


#df_Thermo1.to_csv("thermo1.csv",index=False)


#df_TankStatus.to_csv("tankStatus.csv")





# Write a csv file containing tank temps short term
# Write a csv file containing tank temps long term


# def initialize():
#     global numRows
#     global relaySts
#     numRows = 0
#     temp, hum = (16,30)
#     # Add whether light should start out on or off...
#
#
#     #colString = "Time,Humidity,Temperature"
#     colString = "Time,Humidity,Temperature,HumidifierPower"
#     with open('HumTempData_ShortTerm.csv', 'w') as s:
#         s.write(colString)
#     if not os.path.isfile('HumTempData_LongTerm.csv'):
#         with open('HumTempData_LongTerm.csv', 'w') as s:
#             s.write(colString)