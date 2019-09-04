""" This script runs continuously on a raspberry pi controlling a single box in a
Fitzroy system. This script reads a DHT22 and controls a heating element to control temperature
This script should run inside of a linux screen so as to ensure it continues running after a user
has initialized it.

Note:
    This script must be in the same folder as the configuration file
    config.csv so it can pull pin number values and other such information.

Use Example:
    enter following line in raspberry pi terminal
    python3 run_environmental_control.py 28 80 0.5 8 30 12 00

    The above command starts a Fitzroy box at 28 C, 80% relative humidity, 50% fan power, with sunrise at 8:30 AM,
    and a sunset 12 hours 00 minutes later at 20:30.

Arguments:
    The first positional argument is a floating point number, the target temperature in C
    The second positional argument is a float, the fan duty cycle from 0 - 1.


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

def initiate_light(arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8):
    """
    Opens a new linux screen, starts the sunrisesunset_24h.py script, and detaches.
    """
    argument = str(arg1)+" "+str(arg2)+" "+str(arg3)+" "+str(arg4)+" "+str(arg5)+" "+str(arg6)+" "+str(arg7)+" "+str(arg8)
    os.system("screen -d -m -S light_screen bash -c \"python3 sunrisesunset_24h.py "+argument+"\"")

def turnoff_light():
    """turns off light"""
    os.system("screen kill light_screen")


def retrieve_update_values():
    """ Code that runs once upon startup. Pulls information on
    box configuration from config.csv. Updates settings.csv.

    Returns:
        A dictionary of system parameters specific to this Fitzroy box unit

    """

    parameters = {} #initialize empty dictionary

    # call positional arguments passed to script execution statement
    parameters["tempSetPoint"] = float(sys.argv[1])
    parameters["humiditySetPoint"] = float(sys.argv[2])
    parameters["fanDC"] = float(sys.argv[3])
    #parameters["sunriseTime_hour"] = int(sys.argv[4])
    parameters["sunriseTime"] = datetime.time(int(sys.argv[4]),  int(sys.argv[5]))
    parameters["sunsetTime"] = datetime.time(int(sys.argv[4])+int(sys.argv[6])+floor((int(sys.argv[5])+int(sys.argv[7]))/60),(int(sys.argv[5])+int(sys.argv[7]))%60)
    parameters["photoperiod_h"] = int(sys.argv[6]) + int(sys.argv[7])/60

    #parameters["photoperiod_h"] = int(sys.argv[4])+int(sys.argv[6]) + (int(sys.argv[5])+int(sys.argv[7]))/24


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

    parameters["heater_pid_kp"] = 0.5
    parameters["heater_pid_kd"] = 0
    parameters["heater_pid_ki"] = 0

    parameters["humidifier_pid_kp"] = 0.5
    parameters["humidifier_pid_kd"] = 0
    parameters["humidifier_pid_ki"] = 0

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
    vals = {"Time": None,
            "TemperatureC": temp,
            "Humidity": humidity,
            "HeaterPower": 0,
            "HumidifierPower": 0,
            "FanPower": parameters["fanDC"], #changed this 8/29/2019 - Sam
            "LightPower": 0
            }

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

    pi.set_PWM_dutycycle(parameters["heater_pin"], heater_pulseWidth)
    pi.set_PWM_dutycycle(parameters["humidifier_pin"], humidifier_pulseWidth)
    print("pin power levels updated")


#The main loop
if __name__ == "__main__":

    # set following to True to use fake data and no IO connection
    runningOnPC = False

    #initialize
    parameters = retrieve_update_values()

    print("parameters retrieved from file")
    print(retrieve_update_values())

    max_light_power = 1 #fraction of max light output
    sunrise_duration_min = 5
    sunrise_duration = sunrise_duration_min*60 #seconds

    initiate_light(
        parameters["light_pin"],
        max_light_power,
        sunrise_duration,
        parameters["light_pwm_freq_hz"],
        parameters["sunriseTime"].hour,
        parameters["sunriseTime"].minute,
        parameters["sunsetTime"].hour,
        parameters["sunsetTime"].minute
    )

    #find number of samples to store in short term memory
    maxSamples = floor(parameters["DisplayWindow_sec"]/parameters['LogInterval_sec'])

    #open short term data as a pandas dataframe
    df_s = pd.read_csv('data_shortterm.csv')
    #number of rows of data already stored in short term storage
    numSamples = df_s.shape[0]

    #initialize vals dictionary
    vals = {"Time": None,
            "TemperatureC": "not_connected",
            "Humidity": "not_connected",
            "HeaterPower": "not_connected",
            "HumidifierPower": "not_connected",
            "FanPower": "not_connected",
            "LightPower": "not_connected"
            }

    try:
        # initialize IO pins, sensor
        # query DHT sensor
        print("initialization loop running")

        if not runningOnPC:
            initiate_pigpio()
            pi, s, vals = initializeIO(parameters, vals)
            temp, humidity = query_DHT(s)
            temp_prev = temp
            humidity_prev = humidity
            #s.trigger()
            #temp_prev = s.temperature()
            #humidity_prev = s.humidity()
        else:
            temp_prev, humidity_prev = query_DHT_fakedata()

        # get seconds since start of epoch
        next_reading = time.time()

        print("while loop starting")

        while True:
            # get time
            timeCurrent = datetime.datetime.now()
            timeStamp = timeCurrent.isoformat()
            vals["Time"] = timeStamp


            #query sensor

            if not runningOnPC:
                temp, humidity = query_DHT(s)
            else:
                temp, humidity = query_DHT_fakedata(temp_prev, humidity_prev)


            # make temperature control adjustments
            temp_error = temp-parameters["tempSetPoint"]

            dT = temp - temp_prev
            temp_slope = dT/(parameters['LogInterval_sec']/60) # in degC / minute

            if temp_error > 0:
                heater_DC = 0
            else:
                heater_DC = -1*(temp_error*parameters["heater_pid_kp"]+temp_slope*parameters["heater_pid_kd"])
                if heater_DC > 1:
                    heater_DC = 1
            tempPrev = temp



            # update vals dict
            vals["TemperatureC"] = temp
            vals["HeaterPower"] = heater_DC

            # make humidity control adjustments
            humidity_error = humidity-parameters["humiditySetPoint"]

            dH = humidity - humidity_prev
            humidity_slope = dH/(parameters['LogInterval_sec']/60) # in degC / minute
            if humidity_error > 0:
                humidity_DC = 0
            else:
                humidity_DC = -1*(humidity_error*parameters["humidifier_pid_kp"]+humidity_slope*parameters["humidifier_pid_kd"])
                if humidity_DC > 1:
                    humidity_DC = 1
            humidity_prev = humidity

            # update vals dict
            vals["Humidity"] = humidity
            vals["HumidifierPower"] = humidity_DC

            print("The temp error is:")
            print(temp_error)
            print("The humidity error is:")
            print(humidity_error)


            print(vals)

            # record values in short term memory

            # if short term data not full
            if (numSamples < maxSamples):
                df_s = df_s.append(vals, ignore_index=True)
                df_s.to_csv('data_shortterm.csv', index=False)
                numSamples = numSamples + 1
            else:  # if short term data full
                df_s = df_s.iloc[1:]
                df_s = df_s.append(vals, ignore_index=True)
                df_s.to_csv('data_shortterm.csv', index=False)

            # record values in long term memory
            # COME BACK TO THIS STEP

            #update duty cycle
            if not runningOnPC:
                updateIO(pi,parameters,vals)

            #the query sensor step takes a varying amount of time. Find how much time needed to wait before next sensor query.
            next_reading += parameters['LogInterval_sec']
            sleepTime = next_reading-time.time()
            if sleepTime > 0:
                time.sleep(sleepTime)



    finally:
        print("stopping loop")
        if runningOnPC == False:
            #in case of error or kill process
            pi.set_PWM_dutycycle(parameters["fan_pin"], 0)
            pi.set_PWM_dutycycle(parameters["heater_pin"], 0)
            pi.set_PWM_dutycycle(parameters["humidifier_pin"], 0)
            #pi.write(parameters["humidifier_pin"], 0)
            s.cancel()
            pi.stop()
            turnoff_light()