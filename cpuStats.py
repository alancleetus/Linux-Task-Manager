import re 
import os
import time
from cpu import Cpu
from helperFunctions import readFile, round2, BasicCounter

cpuList=[]
intr = BasicCounter("interrupts")
ctxt = BasicCounter("context switches")
SysWideTime = None
def initCpuList(statFile): 
    """
    This function only runs once to initialize the cpuList. It creates placeholder Cpu objects for the cpuList so they can be used to store all cpu information later in the code. 
    """
    global cpuList
    statsAllCpu = re.findall(r'cpu\d+.* ', statFile)
    for statsForOneCpu in statsAllCpu:
        cpuCols = statsForOneCpu.split()
        cpuName = cpuCols[0]
        tempCpu = Cpu(cpuName)
        cpuList.append(tempCpu)

def getIntrAndCtxt(statFile, readTime):
    global intr
    global ctxt
    intrInfoRow = re.findall(r'intr .*', statFile)[0]
    intr.updateAll(int(intrInfoRow.split(" ")[1]), readTime)

    ctxtInfoRow = re.findall(r'ctxt .*', statFile)[0]
    ctxt.updateAll(int(ctxtInfoRow.split(" ")[1]), readTime)


def parseInfo(statFile, readTime):
    """
    This function takes the information from /proc/stat and parses it for relevant information.

    Parameters:
        statFile (str): The contents of /proc/stat.
        readTime (float): The time at which /proc/stat was read.
    Returns:
        list: Returns a list of Cpu objects for each cpu on the system.
    """
    global cpuList
    try:
        statsAllCpu = re.findall(r'cpu\d+.* ', statFile)
        for statsForOneCpu in statsAllCpu:
            cpuName, utime,_,stime,idle,*_  = statsForOneCpu.split()
            cpuIndex = cpuList.index(Cpu(cpuName))
            cpuList[cpuIndex].updateAll(utime, stime,idle, readTime)
        return cpuList
    except:
        print("Error occurred while parsing cpustat file")
        return []

def fetchAll(): 
    """
    This function reads /proc/stat and sends it to parseInfo() to be processed.

    Returns:
        list: A list of dictionaries holding information for each cpu.
    """
    readTime = time.time()    
    statFile = readFile("/proc/stat")

    if statFile:
        getIntrAndCtxt(statFile, readTime)  
        return [intr, ctxt, parseInfo(statFile, readTime), getSystemWideCpuTime()]
    else:
        print("Error: Unable to retrieve cpu information")
        return None 


def printAll():
    for eachValue in fetchAll():
        print(eachValue) 
    
     
def getSystemWideCpuTime():
    """
    This value is to be used in the procStats.py module to calculate per process cpu utilization.
    """
    global SysWideTime
    sum = 0
    count = 0
    global cpuList
    for eachCpu in cpuList: 
        sum+=eachCpu.sysWideTime
        count+=1
    SysWideTime = sum/count
    return SysWideTime

initCpuList(readFile("/proc/stat"))
fetchAll()
