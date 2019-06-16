"""
A script for recording heating and cooling curves

"""

if __name__ == "__main__":
    import time
    import datetime
    import pigpio
    import DHT22
    import pandas as pd
    from math import floor
    import sys

    """
    This script reads a DHT22 and controls a heating element to control temperature
    The first argument is a floating point number, the target temperature
    The second argument is a float, the fan duty cycle
    Example, to set to 28 C, 50% fan power
    python3 scriptName.py 28 0.5
    """


    tempSetPoint = int(sys.argv[1])
    #fanDC = int(sys.argv[1])


    # Set pins
    df_config = pd.read_csv('config.csv')
    fan_pin = int(df_config["fan_pin"].iloc[0])
    heater_pin = int(df_config["heater_pin"].iloc[0])
    humidifier_pin = int(df_config["humidifier_pin"].iloc[0])
    light_pin = int(df_config["light_pin"].iloc[0])
    DHT22_pin = int(df_config["DHT22_pin"].iloc[0])


    # find information on box config
    df_config = pd.read_csv('config.csv')

    # Intervals of about 2 seconds or less will eventually hang the DHT22.
    INTERVAL = df_config["TempLogInterval_sec"].values[0]
    window = df_config["TempDisplayWindow_sec"].values[0]
    maxSamples = floor(window/INTERVAL) #the number of rows of data to be held in short term storage

    df_s = pd.read_csv('tempData_shortTerm.csv')
    numSamples = df_s.shape[0] #number of rows of data already stored in short term storage

    #controls
    #tempSetPoint = df_config['TempSetPoint'].values[0]
    #tempSetPointList = [26,28,30,32,34]
    i = 0
    #tempSetPoint = 30 #tempSetPointList[i]
    margin = 0

    freq = 10
    k = 1 #proportional control coefficient, if temp is one degree celcius below set point, turn on 100%
    #pi_fan = pigpio.pi()
    # pi_heater = pigpio.pi()
    rt = 24 #room temp
    k2 = 7.14

    pi = pigpio.pi()
    s = DHT22.sensor(pi, DHT22_pin)
    r = 0
    next_reading = time.time()

    pi.set_mode(fan_pin, pigpio.OUTPUT)
    pi.set_mode(heater_pin, pigpio.OUTPUT)
    pi.set_PWM_frequency(heater_pin, freq)

    #initialize fan and heater off
    pi.write(fan_pin, 0)
    pi.write(fan_pin, 1)
    pi.write(heater_pin, 0)
    HeaterStatus = "OFF"
    FanStatus =  "ON"
    tempPrev = 25

    try:
        while True:
            # measure time, temperature, humidity
            timeCurrent = datetime.datetime.now()
            timeStamp = datetime.datetime.now().isoformat()
            r += 1
            s.trigger()
            time.sleep(0.2)
            next_reading += INTERVAL
            sleepTime = next_reading-time.time()
            if sleepTime < 0:
                time.sleep(3)
            else:
                time.sleep(sleepTime) # Overall INTERVAL second polling.
            temp = s.temperature()
            vals = {"Time":timeStamp,
                    "TemperatureC":temp,
                    "Humidity": s.humidity(),
                    "HeaterStatus": HeaterStatus,
                    "HumidifierStatus": "OFF",
                    "FanStatus": FanStatus
                    }
            print(vals)

            #record values in short term memory

            if (numSamples < maxSamples):
                df_s = df_s.append(vals, ignore_index=True)
                df_s.to_csv('tempData_shortTerm.csv', index=False)
                numSamples = numSamples + 1
            else:
                df_s = df_s.iloc[1:]
                df_s = df_s.append(vals, ignore_index=True)
                df_s.to_csv('tempData_shortTerm.csv', index=False)

            #record values in long term memory


            # make control adjustments


            error = temp-tempSetPoint

            dT = temp - tempPrev
            slope = dT/(INTERVAL/60) # in degC / minute


            if error < 0:
                dutyCycle = 1
            else:
                dutyCycle = 0.5 - k2*slope
            if dutyCycle > 1:
                dutyCycle = 1
            elif dutyCycle < 0:
                dutyCycle = 0
            tempPrev = temp

            # dutyCycle = error*k
            # if dutyCycle > 0.9:
            #     dutyCycle = 1
            # elif dutyCycle < 0.1:
            #     dutyCycle =0

            pulseWidth = dutyCycle*255
            pi.set_PWM_dutycycle(heater_pin, pulseWidth)
            HeaterStatus = str(dutyCycle)

            # if (vals["TemperatureC"] < tempSetPoint-margin and (HeaterStatus == "OFF")):
            #     pi.write(heater_pin, 1)
            #     HeaterStatus = "ON"
            #     #pi.write(fan_pin, 0)
            #     #FanStatus = "OFF"
            # elif (vals["TemperatureC"] > tempSetPoint+margin and (HeaterStatus == "ON")):
            #     pi.write(heater_pin, 0)
            #     HeaterStatus = "OFF"
            #     #pi.write(fan_pin, 1)
            #     #FanStatus = "ON"


    finally:
        pi.write(heater_pin, 0)
        pi.write(fan_pin, 0)
        s.cancel()
        pi.stop()