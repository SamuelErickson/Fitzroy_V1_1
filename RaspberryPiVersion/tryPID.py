import time
import random
import matplotlib.pyplot as plt

#https://projects.raspberrypi.org/en/projects/robotPID/9

lst = []
val = 0

k = 0.5 #KP constant
kd = 0.100
ki = 0.015


#Tips: Start my modifying KP constant, then KD, then finally KI
#Make changes in small increments


target =0
time_interval = 1
correction = False
n = 500
error = 0
error_prev = 0
error_sum = 0

for i in range(n):



    ran = random.random()*10 - random.random()*10

    if i % 2 == 0:
        error_prev = error
        error = target - val
        adjustment = error*k+error_prev*kd #+error_sum*ki
        #speed = error * k
        speed = adjustment * time_interval
        error_sum = error_sum + error

    val = val+ran



    if i > n*3/4:
        correction=True

    if correction is True:
        val = val+speed*time_interval

    lst = lst + [val]

    print(val)
    #time.sleep(0.001)


plt.plot(lst)
plt.show()
