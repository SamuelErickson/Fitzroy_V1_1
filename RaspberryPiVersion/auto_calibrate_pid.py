""" Run this script once before activating box no arguments.

Note:
    This script must be in the same folder as the configuration file
    config.csv so it can pull pin number values and other such information.

"""

import time
import datetime
import pigpio
import DHT22
import pandas as pd
from math import floor
import sys
import log_activity as la
import random
import os

def initiate_pigpio():
    """
    Passes a command to linux operating system to start the pigpio daemon
    """
    os.system("sudo pigpiod")


def retrieve_update_values():
    """ Code that runs once upon startup. Pulls information on
    box configuration from config.csv. Updates settings.csv.

    Returns:
        A dictionary of system parameters specific to this Fitzroy box unit

    """

    parameters = {} #initialize empty dictionary

    # call positional arguments passed to script execution statement
    parameters["tempSetPoint"] = "NA"
    parameters["humiditySetPoint"] = "NA"
    parameters["fanDC"] = "NA"
    parameters["sunriseTime"] = "NA"
    parameters["sunsetTime"] = "NA"
    parameters["photoperiod_h"] = "NA"

    #open the config.csv and create a pandas dataframe
    df_config = pd.read_csv('config.csv')
    #retrieve values, save in parameters dictionary
    parameters['fan_pin'] = int(df_config["fan_pin"].iloc[0])
    parameters['heater_pin'] = int(df_config["heater_pin"].iloc[0])
    parameters['humidifier_pin'] = int(df_config["humidifier_pin"].iloc[0])
    parameters['light_pin'] = int(df_config["light_pin"].iloc[0])
    parameters['DHT22_pin'] = int(df_config["DHT22_pin"].iloc[0])

    #open the settings.csv and create a pandas dataframe
    df_settings = pd.read_csv('settings.csv')

    #update the file settings.csv
    df_settings['TempSetPoint'] = parameters["tempSetPoint"]

    #data display settings

    #five second default sampling period
    parameters['LogInterval_sec'] = 5

    #24 hours default data display window for desktop interface
    parameters["DisplayWindow_sec"] = 86400

    #INITIALIZE CONTROL PARAMETERS
    #Pulse width modulation frequencies

    parameters["humidifier_pwm_freq_hz"] = 10 #NEW LINE
    parameters["heater_pwm_freq_hz"] = 10
    parameters["fan_pwm_freq_hz"] = 10
    parameters["light_pwm_freq_hz"] = 500

    #PID (Proportional-Derivative-Integral) gains

    parameters["heater_pid_kp"] = 0
    parameters["heater_pid_kd"] = 0
    parameters["heater_pid_ki"] = 0

    parameters["humidifier_pid_kp"] = 0
    parameters["humidifier_pid_kd"] = 0
    parameters["humidifier_pid_ki"] = 0

    parameters["fan_pid_kp"] = 0
    parameters["fan_pid_kd"] = 0
    parameters["fan_pid_ki"] = 0

    # Intervals of about 2 seconds or less will eventually hang the DHT22.
    df_settings['LogInterval_sec'] = [parameters['LogInterval_sec']]
    df_settings["DisplayWindow_sec"] = [parameters["DisplayWindow_sec"]]
    df_settings['LightsOnTime'] = [parameters["sunriseTime"]]
    df_settings['LightsOffTime'] = [parameters["sunsetTime"]]
    df_settings["Photoperiod (h)"] = parameters["photoperiod_h"]
    df_settings.to_csv("settings.csv", index=False)

    return(parameters)


def initializeIO(parameters,vals):
    """
    initializes and returns new pigpio pi object for controlling pins
    """
    pi = pigpio.pi()

    # initialize DHT sensor object
    s = DHT22.sensor(pi, parameters["DHT22_pin"])

    #test DHT22
    s.trigger()
    time.sleep(5)
    temp = s.temperature()
    humidity = s.humidity()
    print("testing DHT22 sensor")
    print("temp is "+str(temp)+" and humidity is "+str(humidity))

    # initialize humidifier binary power output
    #pi.set_mode(parameters['humidifier_pin'], pigpio.OUTPUT)

    pi.set_PWM_frequency(parameters['heater_pin'], parameters["heater_pwm_freq_hz"])
    pi.set_PWM_frequency(parameters['fan_pin'], parameters["fan_pwm_freq_hz"])
    #pi.set_PWM_frequency(parameters['light_pin'], parameters["light_pwm_freq_hz"])

    # start fan at power level specified on starting command
    pi.set_PWM_dutycycle(parameters['fan_pin'], int(255* parameters["fanDC"]))
    #Ben edited this 8-28
    #pi.set_PWM_frequency(parameters['humidifier_pin'], 0) - not correct talk to Sam about this
    #pi.set_PWM_dutycycle(parameters['light_pin'], 0)

    # heater, humidifier off
    pi.set_PWM_dutycycle(parameters['heater_pin'], 0)
    pi.set_PWM_dutycycle(parameters['humidifier_pin'], 0)

    # SAM - fix below, instead of defining new dictionary, simply edit existing values

    # Edit vals dictionary
    vals["TemperatureC"] = temp
    vals["Humidity"] = humidity
    vals["HeaterPower"] = 0
    vals["HumidifierPower"] = 0
    vals["FanPower"] = 0
    vals["LightStatus"] = "Not_Recorded"

    return pi, s, vals

def query_DHT(s):
    """
    Pass sensor object
    returns temperature, humidity
    """
    s.trigger()
    time.sleep(1)
    temp = s.temperature()
    humidity = s.humidity()
    return temp, humidity


def query_DHT_fakedata(temp_previous = 20, hum_previous=80):
    """
    returns random temperature, humidity +/- 1 from previous values passed as arguments
    """
    temperature = temp_previous + random.random()*1 - random.random()*1
    humidity = hum_previous + random.random()*1 - random.random()*1
    return (temperature,humidity)

def updateIO(pi,parameters,vals):
    heater_pulseWidth = vals["HeaterPower"]*255
    humidifier_pulseWidth = vals["HumidifierPower"]*255
    fan_pulseWidth = vals["FanPower"]*255

    pi.set_PWM_dutycycle(parameters["heater_pin"], heater_pulseWidth)
    pi.set_PWM_dutycycle(parameters["humidifier_pin"], humidifier_pulseWidth)
    pi.set_PWM_dutycycle(parameters["fan_pin"], fan_pulseWidth)

    print("pin power levels updated")



#The main loop
if __name__ == "__main__":


    #initialize parameters
    parameters = retrieve_update_values()
    #find number of samples to store in short term memory
    maxSamples = floor(parameters["DisplayWindow_sec"]/parameters['LogInterval_sec'])
    #open short term data as a pandas dataframe
    df_s = pd.read_csv('data_calibration.csv')
    #number of rows of data already stored in short term storage
    numSamples = df_s.shape[0]

    #initialize vals dictionary. vals represents values that will change over the course of operation of the device, in contrast to settings and parameters.
    vals = {"Time": None,
            "TempSetPoint": "NA",
            "HumiditySetPoint": "NA",
            "TemperatureC": "NA",
            "Humidity": 0,
            "HeaterPower": 0,
            "HumidifierPower": 0,
            "FanPower": 0,
            "LightStatus": 0
            }


    #
    runningOnPC = False
    try:

        # initialize IO pins, sensor
        print("initialization loop running")
        if not runningOnPC:
            initiate_pigpio()
            pi, s, vals = initializeIO(parameters, vals)
            temp, humidity = query_DHT(s)
            temp_prev = temp
            temp_error_integral = 0
            humidity_prev = humidity
            #s.trigger()
            #temp_prev = s.temperature()
            #humidity_prev = s.humidity()
        else:
            temp_prev, humidity_prev = query_DHT_fakedata()
        # get seconds since start of epoch
        next_reading = time.time()

        #Initialize PID heater terms
        parameters["heater_pid_kp"] = 0
        parameters["heater_pid_ki"] = 0
        parameters["heater_pid_kd"] = 0

        #Plan calibration strategy
        period_kd = 45/parameters['LogInterval_sec'] #number of periods to wait before changing kd term (45 seconds, so 15 sampling periods)
        period_count = 0
        increment_kd = 0.05 #the amount to increase kd every period_kd number of sample periods
        parameters["tempSetPoint"] = 28 #temp set point 28C.



        #Calibrate heater
        print("Calibrating heater without fan")
        print("while loop starting")
        calibrating_heater = True
        while calibrating_heater:
            # increment count of sampling periods
            period_count =+ 1


            # Describe the strategy, order of steps for calibration
            adjusting_heater_kd = True #working on kd for heater
            if adjusting_heater_kd:
                if period_count < period_kd: #Allow for one sampling period with no adjusting first
                    adjust_heater = False
                else:
                    adjust_heater = True
                if period_count%period_kd==0: #Check whether it is time to increase the kd
                    parameters["heater_pid_kd"] =+ increment_kd
                    print("incrementing kd")
                    print(parameters["heater_pid_kd"])

            # get time
            timeCurrent = datetime.datetime.now()
            timeStamp = timeCurrent.isoformat()
            vals["Time"] = timeStamp

            # query DHT sensor
            if not runningOnPC:
                temp, humidity = query_DHT(s)
            else:
                temp, humidity = query_DHT_fakedata(temp_prev, humidity_prev)

            # make temperature control adjustments
            temp_error = temp - parameters["tempSetPoint"]
            dT = temp - temp_prev
            temp_slope = dT / (parameters['LogInterval_sec'] / 60)  # in degC / minute
            temp_error_integral = temp_error_integral+temp_error #sum of all temp_error over time

            # Print the standard deviation from the last period_kd number of sample periods
            if adjust_heater:
                print("printing temperature data, last 5 measurements")
                std_dev = df_s["TemperatureC"].iloc[-5:].to_list()

            # Determine power supplied to heater
            if False:
                if temp_error > 0:
                    heater_DC = 0

                else:
                    heater_DC = -1 * (temp_error * parameters["heater_pid_kp"] + temp_slope * parameters["heater_pid_kd"])
                    if heater_DC > 1:
                        heater_DC = 1
                tempPrev = temp
                vals["HeaterPower"] = heater_DC

            # update vals dict
            vals["TemperatureC"] = temp

            # print status to console
            print("The temp error is:")
            print(temp_error)
            print(vals)

            # record values in short term memory

            # if short term data not full
            if (numSamples < maxSamples):
                df_s = df_s.append(vals, ignore_index=True)
                df_s.to_csv('data_calibration.csv', index=False)
                numSamples = numSamples + 1
            else:  # if short term data full
                df_s = df_s.iloc[1:]
                df_s = df_s.append(vals, ignore_index=True)
                df_s.to_csv('data_calibration.csv', index=False)

            # record values in long term memory
            # COME BACK TO THIS STEP

            # update duty cycle
            if not runningOnPC:
                updateIO(pi, parameters, vals)

            # the query sensor step takes a varying amount of time. Find how much time needed to wait before next sensor query.
            next_reading += parameters['LogInterval_sec']
            sleepTime = next_reading - time.time()
            if sleepTime > 0:
                time.sleep(sleepTime)




    #if an error is thrown in the try block, the script will skip to this finally block and execute before exiting
    finally:
        print("stopping loop")
        if runningOnPC == False:
            #in case of error or kill process
            pi.write(parameters["fan_pin"], 0)
            pi.write(parameters["heater_pin"], 0)
            pi.write(parameters["humidifier_pin"], 0)
            #pi.write(parameters["humidifier_pin"], 0)
            s.cancel()
            pi.stop()



# #The main loop
# if __name__ == "__main__":
#
#     # set following to True to use fake data and no IO connection
#     runningOnPC = False
#
#     #initialize parameters
#     parameters = retrieve_update_values()
#
#     print("parameters retrieved from file")
#     print(retrieve_update_values())
#
#     #find number of samples to store in short term memory
#     maxSamples = floor(parameters["DisplayWindow_sec"]/parameters['LogInterval_sec'])
#     #open short term data as a pandas dataframe
#     df_s = pd.read_csv('data_calibration.csv')
#     #number of rows of data already stored in short term storage
#     numSamples = df_s.shape[0]
#
#     #initialize vals dictionary
#     vals = {"Time": None,
#             "TempSetPoint": parameters["tempSetPoint"],
#             "HumiditySetPoint": parameters["humiditySetPoint"],
#             "TemperatureC": "not_connected",
#             "Humidity": "not_connected",
#             "HeaterPower": "not_connected",
#             "HumidifierPower": "not_connected",
#             "FanPower": "not_connected",
#             "LightStatus": "not_connected"
#             }
#
#     try:
#         # initialize IO pins, sensor
#         # query DHT sensor
#         print("initialization loop running")
#
#         if not runningOnPC:
#             initiate_pigpio()
#             pi, s, vals = initializeIO(parameters, vals)
#             temp, humidity = query_DHT(s)
#             temp_prev = temp
#             humidity_prev = humidity
#             #s.trigger()
#             #temp_prev = s.temperature()
#             #humidity_prev = s.humidity()
#         else:
#             temp_prev, humidity_prev = query_DHT_fakedata()
#
#         #initialize fan_DC
#         fan_DC = parameters["fanDC"]
#
#         # get seconds since start of epoch
#         next_reading = time.time()
#
#         print("Calibrating heater without fan")
#         print("while loop starting")
#
#         while True:
#             # get time
#             timeCurrent = datetime.datetime.now()
#             timeStamp = timeCurrent.isoformat()
#             vals["Time"] = timeStamp
#
#
#             #query sensor
#
#             if not runningOnPC:
#                 temp, humidity = query_DHT(s)
#             else:
#                 temp, humidity = query_DHT_fakedata(temp_prev, humidity_prev)
#
#
#             # make temperature control adjustments
#             temp_error = temp-parameters["tempSetPoint"]
#
#             dT = temp - temp_prev
#             temp_slope = dT/(parameters['LogInterval_sec']/60) # in degC / minute
#
#             if temp_error > 0:
#                 heater_DC = 0
#                 fan_DC =(temp_error*parameters["fan_pid_kp"]+temp_slope*parameters["fan_pid_kd"])
#                 if fan_DC < 0.1:
#                     fan_DC = 0
#                 elif fan_DC > 1:
#                     fan_DC = 1
#             else:
#                 heater_DC = -1*(temp_error*parameters["heater_pid_kp"]+temp_slope*parameters["heater_pid_kd"])
#                 if heater_DC > 1:
#                     heater_DC = 1
#             tempPrev = temp
#
#
#
#             # update vals dict
#             vals["TemperatureC"] = temp
#             vals["HeaterPower"] = heater_DC
#             vals["FanPower"] = fan_DC
#
#             # make humidity control adjustments
#             humidity_error = humidity-parameters["humiditySetPoint"]
#
#             dH = humidity - humidity_prev
#             humidity_slope = dH/(parameters['LogInterval_sec']/60) # in degC / minute
#             if humidity_error > 0:
#                 humidity_DC = 0
#             else:
#                 humidity_DC = -1*(humidity_error*parameters["humidifier_pid_kp"]+humidity_slope*parameters["humidifier_pid_kd"])
#                 if humidity_DC > 1:
#                     humidity_DC = 1
#             humidity_prev = humidity
#
#             # update vals dict
#             vals["Humidity"] = humidity
#             vals["HumidifierPower"] = humidity_DC
#
#
#             #print status to console
#             print("The temp error is:")
#             print(temp_error)
#             print("The humidity error is:")
#             print(humidity_error)
#             print(vals)
#
#             # record values in short term memory
#
#             # if short term data not full
#             if (numSamples < maxSamples):
#                 df_s = df_s.append(vals, ignore_index=True)
#                 df_s.to_csv('data_shortterm.csv', index=False)
#                 numSamples = numSamples + 1
#             else:  # if short term data full
#                 df_s = df_s.iloc[1:]
#                 df_s = df_s.append(vals, ignore_index=True)
#                 df_s.to_csv('data_shortterm.csv', index=False)
#
#             # record values in long term memory
#             # COME BACK TO THIS STEP
#
#             #update duty cycle
#             if not runningOnPC:
#                 updateIO(pi,parameters,vals)
#
#             #the query sensor step takes a varying amount of time. Find how much time needed to wait before next sensor query.
#             next_reading += parameters['LogInterval_sec']
#             sleepTime = next_reading-time.time()
#             if sleepTime > 0:
#                 time.sleep(sleepTime)
#
#
#
#     finally:
#         print("stopping loop")
#         if runningOnPC == False:
#             #in case of error or kill process
#             pi.write(parameters["fan_pin"], 0)
#             pi.write(parameters["heater_pin"], 0)
#             pi.write(parameters["humidifier_pin"], 0)
#             #pi.write(parameters["humidifier_pin"], 0)
#             s.cancel()
#             pi.stop()
#             turnoff_light()