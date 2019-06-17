"""
This module provides a function for recording error messages and user
activity in a text file for debugging/troubleshooting
"""


import time
import os

def log_activity(fileName,errorMessage = "executed"):
    """
    records time, name of script and appends to activity_log.txt file
    To record the execution of a script, call this function with __file__ as the argument
    To record an error message, add an additional optional keyword argument errorMessage

    Examples:

    import log_activity as la

    la.recordActivity(__file__)

    try:
        a = 3+"can I concatenate a string and an int?"
    except Exception as err:
        log_activity(__file__, errorMessage=str(err))

    Two lines are recorded in the error log file

    Mon Jun 17 09:11:03 2019,log_activity.py,executed
    Mon Jun 17 09:11:03 2019,log_activity.py,unsupported operand type(s) for +: 'int' and 'str'

    """
    note = os.path.basename(fileName)
    timeNow = time.asctime()
    note = timeNow + "," + note+ ","+errorMessage+"\n"
    f = open("activity_log.txt", 'a+')
    f.writelines(note)
    f.close()

