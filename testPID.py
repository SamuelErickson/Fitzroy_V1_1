from simple_pid import PID
import time
#pid = PID(1,0.1,0.05,setpoint=1)



#v = controlled_system.update(0)

#while True:
#    control = pid(v)
#    v = controlled_system.update(control)


output = pid(current_value)
pid.sample_time = 0.01

while True:
    output = pid(current_value)
        



#sleep(1)