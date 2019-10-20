"""
memStats.py: This module retrieves the memory statistics for the system the program is being run on. Namely the amount of available and total RAM in MB and also the utilization of RAM in percentage. 
"""

import re
from helperFunctions import readFile, round2

memInfo = {"memTotal":None, "memAvail":None, "memUtil":None}
    
def parseInfo(memFile):  
    """
    This function parses the contents of /proc/meminfo and returns the memory information in a dictionary.

    Parameters:
        memFile (str): The contents of /proc/meminfo

    Returns 
        dictionary: A dictionary that holds the available memory  in MB, total memory in MB, and the memory utilization in percentage.

    """
    
    memTotal = memAvail = memTotal = 0
    
    try:
        # get the MemTotal value and convert it to MB from kB
        memTotal = float(re.findall(r'MemTotal: .*', memFile)[0].split(" ")[-2])
        memTotal = memTotal/1024
    except:
        print("Error: Unable to retrieve MemTotal")
        
    try:
        # get the MemAvailable value and convert it to MB from kB
        memAvail = float(re.findall(r'MemAvailable: .*', memFile)[0].split(" ")[-2])
        memAvail = memAvail/1024
    except: 
        print("Error: Unable to retrieve memAvail")
    
    try:
        # calculate memory utilization
        memUtil = ((memTotal-memAvail)/memTotal)*100
        memInfo = {"memTotal":memTotal, "memAvail":memAvail, "memUtil":memUtil}
    except:
        print("Error: Unable to calculate memUtil")

    return memInfo 


def fetchAll():
    """
    This function reads /proc/meminfo and sends it to parseInfo() to be processed.

    Returns:
        dictionary: Dictionary holding memory information.
    """
    memFile = readFile("/proc/meminfo")
    if memFile:
        return parseInfo(memFile)
    else:
        print("Error: Unable to retrieve memory information")
        return None 

def printAll():
    for k, v in fetchAll().items():
        if k == "memUtil":
            print(" {}: {}%".format(k, round2(float(v))))
        else:
            print(" {}: {} MB".format(k, round2(float(v))))

# initialize the memInfo Dictionary
fetchAll()

#printAll()