import os
import re
import pwd
import time
import subprocess
from stat import *
from process import Process 
from helperFunctions import readFile, round2, BasicCounter

processDict = {}
inodeDict = {}
sysWideCpuTime = 0
vMemTotal = None
phyMemTotal = None
pageSize = None
def setSysWideCpuTime(time):
    global sysWideCpuTime
    sysWideCpuTime = time


def setPhyMemTotal(valInMB):
    global phyMemTotal
    if phyMemTotal:
        return phyMemTotal
    else:
        phyMemTotal = valInMB*1024*1024/int(pageSize) #convert to bytes then to total number of pages
        return phyMemTotal

def getPageSize():
    global pageSize
    if pageSize:
        return pageSize
    else:
        pageSize = subprocess.check_output(["getconf","PAGE_SIZE"]).decode("utf-8")
        return (int)(pageSize)

getPageSize()

def calculateVmemTotal():
    global vMemTotal
    
    if vMemTotal:
        return vMemTotal
    else:
        try:
            architecture = subprocess.check_output(["uname","-m"]).decode("utf-8")
            if "64" in architecture:
                vMemTotal = 2**64 #TODO: check this
            else:
                vMemTotal = 2**32 
        except:
            print("Error: getting vmem total")
    
    return vMemTotal


def getAllPids():
    try:
        return set(filter(lambda dir: str.isdigit(dir), os.listdir("/proc")))
    except:
        print("Error: Unable to get all PIDs")


def getPID(inodeNumber):
    global inodeDict
    return inodeDict[inodeNumber]


def parseInodeNumber(pid): 
    inodeVal = -1
    try:       
        path = "/proc/"+pid+"/fd"
        inner = os.listdir(path)  
        for fileName in inner: 
            if str.isdigit(fileName): 
                innerpath="/proc/"+pid+"/fd/"+fileName  
                if S_ISSOCK(os.stat(innerpath).st_mode):
                    global inodeDict
                    inodeDict[str(os.stat(innerpath).st_ino)] = pid
                    inodeVal = str(os.stat(innerpath).st_ino)
                 
    except:
        #print("No inode number found for PID:", pid)
        return inodeVal
    return inodeVal


def parseInfo(pid, statFile, statusFile, readTime):
    try:
        try:
            statFile = statFile.split()
            name = statFile[1][1:-1]          
            userMode = statFile[13]
            sysMode = statFile[14]
            vmem = statFile[22]
            rss = statFile[23]
        except:
            print("Error: parsing /proc/{}/stat file".format(pid))
            return None

        userName= "" 
        try:
            uid = re.findall(r'Uid:\s+\d+\s',statusFile)[0].split()[1]  
            userName = pwd.getpwuid(int(uid)).pw_name 
        except:
            print("Error: trying to get userName")

        inodeNumber = parseInodeNumber(pid) 
        
        if pid in processDict:
            processDict[pid].updateAll(name, userName, inodeNumber, userMode, sysMode, vmem, rss, readTime)
            return processDict[pid]
        else: 
            temp_process = Process(pid)
            temp_process.updateAll(name, userName, inodeNumber, userMode, sysMode, vmem, rss, readTime)
            return temp_process
    except:
        print("Error: process parsing information")
        return None
    

def fetchAll():
    pidSet = getAllPids()
    
    try:
        global processDict
        global inodeDict
        for pid in pidSet:
            if os.path.exists("/proc/"+pid):
                readTime = time.time()
                statFile = readFile("/proc/"+pid+"/stat")
                statusFile = readFile("/proc/"+pid+"/status")
                
                temp_process = parseInfo(pid, statFile, statusFile, readTime)
                #print(temp_process)
                if temp_process:
                    processDict[pid]=temp_process
        return processDict 
          
    except:
        print("Error: FetchAll error in processStat.py")
        return {}


def printAll():
    global sysWideCpuTime
    global phyMemTotal
    global vMemTotal
    print("\n|{:>6}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|".format(
            "pid", "Program", "UserName", "Inode Number", "User Util", "Sys Util", "Total Util", "Vmem Util", "Phy Mem Util"))
    print("|{:>6}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|".format("","","", "", "", "", "", "", ""))
    
    for pid, eachProcess in fetchAll().items():
        cpu = eachProcess.calculateCpuUtilization(sysWideCpuTime)
        print("|{:>6}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|".format(
            eachProcess.pid,
            eachProcess.name,
            eachProcess.userName,
            eachProcess.inodeNumber,
            cpu["userMode"],
            cpu["sysMode"],
            cpu["total"], 
            eachProcess.calculateVmemUtil(vMemTotal),
            eachProcess.calculatePhyMemUtil(phyMemTotal)))
 
 
    #print(sysWideCpuTime)
        
