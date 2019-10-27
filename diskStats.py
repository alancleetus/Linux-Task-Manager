"""
This module retrieves the intervalized disk data. Namely the disk reads/writes, the block reads/writes 
"""

import re
import time
from disk import Disk
from helperFunctions import readFile, round2

diskList=[]

def initDiskList(diskStatsFile): 
    """
    This function only runs once to initialize the diskList. It creates placeholder Disk objects for the diskList so they can be used to store all disk information later in the code. 
    """
    global diskList
    statsAllDisks = re.findall(r'.*sd[a-z] .*', diskStatsFile)
    for statsForOneDisk in statsAllDisks:
        diskCols = statsForOneDisk.split()
        diskName = diskCols[2]
        tempDisk = Disk(diskName)
        diskList.append(tempDisk)


def parseInfo(diskStatsFile, readTime): 
    """
    This function takes the information from /proc/diskstats and parses it for relevant information.

    Parameters:
        diskStatsFile (str): The contents of /proc/diskstats.
        readTime (float): The time at which /proc/diskstats was read.
    Returns:
        list: Returns a list of Disk objects for each disk on the system.
    """
    global diskList
    try:
        statsAllDisks = re.findall(r'.*sd[a-z] .*', diskStatsFile)
        for statsForOneDisk in statsAllDisks:
            diskCols = statsForOneDisk.split()
            
            diskName = diskCols[2]
            diskIndex = diskList.index(Disk(diskName))

            diskList[diskIndex].updateAll(int(diskCols[4]), int(diskCols[8]), int(diskCols[6]), int(diskCols[10]), readTime)
        return diskList
    except:
        print("Error occurred while parsing diskstat file")
        return []
        
def fetchAll(): 
    """
    This function reads /proc/diskstats and sends it to parseInfo() to be processed.

    Returns:
        list: A list of dictionaries holding disk/block read/write per disk.
    """
    readTime = time.time()    
    diskStatsFile = readFile("/proc/diskstats")

    if diskStatsFile:
        return parseInfo(diskStatsFile, readTime)
    else:
        print("Error: Unable to retrieve disk information")
        return None 


def printAll():
    for eachDisk in fetchAll():
        print(eachDisk)

# initialize the diskList
initDiskList(readFile("/proc/diskstats"))
fetchAll()

#print(printAll()) 