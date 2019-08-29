import os

# This shell script runs the commands needed to start one Fitzroy system unit box



#    Example: python3 run_environmental_control.py 28 80 0.5 8 30 12 00
#    The below command starts a Fitzroy box at 28 C, 80% relative humidity, 50% fan power, with sunrise at 8:30 AM,
#    and a sunset 12 hours 00 minutes later at 20:30.

os.system("screen -d -m -S environmental_control bash -c \"python3 run_environmental_control.py 28 80 0 14 54 1 44\"")
