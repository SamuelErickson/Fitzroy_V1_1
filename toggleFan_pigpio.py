"""
A script for recording heating and cooling curves

"""

if __name__ == "__main__":
    from time import sleep
    #import datetime
    import pigpio
    #import DHT22
    #import pandas as pd
    from math import floor

    # Set pins
    heater_pin = 4
    fan_pin = 17

    pi = pigpio.pi()

    pi.set_mode(fan_pin, pigpio.OUTPUT)
    pi.set_mode(heater_pin, pigpio.OUTPUT)

    #initialize fan and heater off
    pi.write(fan_pin, 0)
    pi.write(heater_pin, 0)
    HeaterStatus = "OFF"
    FanStatus =  "OFF"

    sleep(2)
    if pi.read(fan_pin) == 0:
        pi.write(fan_pin, 1)
        FanStatus =  "ON"
        print("Fan is "+FanStatus)
        sleep(2)
    for i in range(4):
        if pi.read(heater_pin) == 0:
            pi.write(heater_pin, 1)
            HeaterStatus = "ON"
            print("Heat is " + HeaterStatus)
            sleep(15)
        elif pi.read(heater_pin) == 1:
            pi.write(heater_pin, 0)
            HeaterStatus = "OFF"
            print("Heat is " + HeaterStatus)
            sleep(1)
        else:
            print("error")


    # if (HeaterStatus == "OFF"):
    #     pi.write(heater_pin, 1)
    #     HeaterStatus = "ON"
    #     i = i+1
    #
    #     tempSetPoint = tempSetPointList[i]
    #     print("i = "+str(i)+" tempsetpoint:"+str(tempSetPoint))
    #     #pi.write(fan_pin, 0)
    #     #FanStatus = "OFF"
    # elif (vals["TemperatureC"] > tempSetPoint and (HeaterStatus == "ON")):
    #     pi.write(heater_pin, 0)
    #     HeaterStatus = "OFF"
    #     i = i+1
    #     tempSetPoint = tempSetPointList[i]
    #     print("i = " + str(i) + " tempsetpoint:" + str(tempSetPoint))
    #     #pi.write(fan_pin, 1)
    #     #FanStatus = "ON"


    pi.write(heater_pin, 0)
    pi.write(fan_pin, 0)
    FanStatus =  "OFF"

    print("Fan is "+FanStatus)

    pi.stop()