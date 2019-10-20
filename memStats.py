"""
memStats.py: This module retrieves the memory statistics for the system the program is being run on. Namely the amount of available and total RAM in MB and also the utilization of RAM in percentage. 
"""

import re
import time
from helperFunctions import readFile, round2, BasicGauge

memAvail = BasicGauge("memAvail")

memTotal = 0

def parseInfo(memFile, readTime):  
    """
    This function parses the contents of /proc/meminfo and returns the memory information in a dictionary.

    Parameters:
        memFile (str): The contents of /proc/meminfo

    Returns 
        list: A list that holds the available memory as a BasicGauge object, total memory in MB, and the memory utilization in percentage.

    """
    # TODO: you only need to do this once because the size of memory doesn't dynamically change 
    try:
        # get the MemTotal value and convert it to MB from kB
        memTotal = float(re.findall(r'MemTotal: .*', memFile)[0].split(" ")[-2])
        memTotal = memTotal/1024
    except:
        print("Error: Unable to retrieve MemTotal")
        memTotal = 0
        
    try:
        # get the MemAvailable value and convert it to MB from kB
        avail = float(re.findall(r'MemAvailable: .*', memFile)[0].split(" ")[-2])
        avail = avail/1024

        memAvail.updateAll(avail, readTime)
    except: 
        print("Error: Unable to retrieve memAvail")
    
    try:
        # calculate memory utilization
        memUtil = round2((memAvail.calculateAverage()/memTotal)*100)
    except:
        print("Error: Unable to calculate memUtil")
        memUtil = 0

    return [memTotal, memAvail, memUtil] 


def fetchAll():
    """
    This function reads /proc/meminfo and sends it to parseInfo() to be processed.

    Returns:
        dictionary: Dictionary holding memory information.
    """
    readTime = time.time()
    memFile = readFile("/proc/meminfo")
    if memFile:
        return parseInfo(memFile, readTime)
    else:
        print("Error: Unable to retrieve memory information")
        return None 

def printAll():
    for i in fetchAll():
        print(i)

# initialize the memInfo Dictionary
fetchAll()

#printAll()
