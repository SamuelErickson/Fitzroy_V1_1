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
    heater_pin = 27
    humidifier_pin = 25

    pi = pigpio.pi()

    pi.set_mode(humidifier_pin, pigpio.OUTPUT)
    pi.set_mode(heater_pin, pigpio.OUTPUT)

    #initialize fan and heater off
    pi.write(humidifier_pin, 0)
    pi.write(heater_pin, 0)
    HumidifierStatus = "OFF"
    FanStatus =  "OFF"

    sleep(2)
    if pi.read(humidifier_pin) == 0:
        pi.write(humidifier_pin, 1)
        FanStatus =  "ON"
        print("Fan is "+FanStatus)
        sleep(2)
    for i in range(4):
        if pi.read(humidifier_pin) == 0:
            pi.write(humidifier_pin, 1)
            HumidifierStatus = "ON"
            print("Heat is " + HumidifierStatus)
            sleep(15)
        elif pi.read(humidifier_pin) == 1:
            pi.write(humidifier_pin, 0)
            HumidifierStatus = "OFF"
            print("Heat is " + HumidifierStatus)
            sleep(1)
        else:
            print("error")


    # if (HumidifierStatus == "OFF"):
    #     pi.write(heater_pin, 1)
    #     HumidifierStatus = "ON"
    #     i = i+1
    #
    #     tempSetPoint = tempSetPointList[i]
    #     print("i = "+str(i)+" tempsetpoint:"+str(tempSetPoint))
    #     #pi.write(humidifier_pin, 0)
    #     #FanStatus = "OFF"
    # elif (vals["TemperatureC"] > tempSetPoint and (HumidifierStatus == "ON")):
    #     pi.write(heater_pin, 0)
    #     HumidifierStatus = "OFF"
    #     i = i+1
    #     tempSetPoint = tempSetPointList[i]
    #     print("i = " + str(i) + " tempsetpoint:" + str(tempSetPoint))
    #     #pi.write(humidifier_pin, 1)
    #     #FanStatus = "ON"


    pi.write(heater_pin, 0)
    pi.write(humidifier_pin, 0)
    FanStatus =  "OFF"

    print("Fan is "+FanStatus)

    pi.stop()