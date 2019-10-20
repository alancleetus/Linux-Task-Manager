import re 
import os
import time
from cpu import Cpu
from helperFunctions import readFile, round2, BasicCounter

cpuList=[]
intr = BasicCounter("interrupts")
ctxt = BasicCounter("context switches")

def initCpuList(statFile): 
    """
    This function only runs once to initialize the cpuList. It creates placeholder Cpu objects for the cpuList so they can be used to store all cpu information later in the code. 
    """
    statsAllCpu = re.findall(r'cpu\d+.* ', statFile)
    for statsForOneCpu in statsAllCpu:
        cpuCols = statsForOneCpu.split()
        cpuName = cpuCols[0]
        tempCpu = Cpu(cpuName)
        cpuList.append(tempCpu)

def getIntrAndCtxt(statFile, readTime):
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
        return [intr, ctxt, parseInfo(statFile, readTime)]
    else:
        print("Error: Unable to retrieve cpu information")
        return None 


def printAll():
    for eachCpu in fetchAll():
        print(eachCpu)

initCpuList(readFile("/proc/stat"))
fetchAll()

"""
sysWideTime = 0

intrData = {"prev":0, "curr":0}
ctxtData = {"prev":0, "curr":0}
cpuData = {"prev":{}, "curr":{}}

lastIntrReadTime = {"prev":0,"curr":0}
lastCtxtReadTime = {"prev":0,"curr":0}
lastCpuReadTime = {"prev":0,"curr":0}
 
##########################################################
                    #######INTR INFO#########
########################################################## 
def getIntr(): 
    lastIntrReadTime["prev"] = lastIntrReadTime["curr"]
    lastIntrReadTime["curr"] = time.time()
    statFile = readFile("/proc/stat")

    intrData["prev"] = intrData["curr"]
    intrInfoRow = re.findall(r'intr .*', statFile)[0]
    intrData["curr"] = int(intrInfoRow.split(" ")[1])

    return intrData["curr"]

def getIntrFreq():
    getIntr()

    timeInterval = lastIntrReadTime["curr"]-lastIntrReadTime["prev"]
    freq = (intrData["curr"]-intrData["prev"])/timeInterval
    return freq

##########################################################
                    #######CTXT INFO#########
##########################################################
def getCtxt(): 
    lastCtxtReadTime["prev"] = lastCtxtReadTime["curr"]
    lastCtxtReadTime["curr"] = time.time() 
    statFile = readFile("/proc/stat")

    ctxtData["prev"] = ctxtData["curr"]
    ctxtInfoRow = re.findall(r'ctxt .*', statFile)[0]
    ctxtData["curr"] = int(ctxtInfoRow.split(" ")[1]) 
    return ctxtData["curr"]
    

def getCtxtFreq(): 
    getCtxt() 
    timeInterval = lastCtxtReadTime["curr"]-lastCtxtReadTime["prev"]
    freq = (ctxtData["curr"]-ctxtData["prev"])/timeInterval
    return freq

##########################################################
             #######My Functions#########
##########################################################
def fetchAll(): 
    return [getIntrFreq(), getCtxtFreq(), getCpuUtil()]
 
def getSystemWideCpu():
    return sysWideTime()
    
def intializeValues():
    getIntr()
    getCtxt()
    getCpus()

intializeValues()
"""
