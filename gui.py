"""
Author: Alan Cleetus
"""
import eel
import memStats
import diskStats
import cpuStats
import processStats
import netStats
import tcpUdpConnStats 
from helperFunctions import round2, readFile
import subprocess

eel.init('web')

TIME_INTERVAL = 1

KEYLOGGER_ON = False

@eel.expose
def setTimeInterval(timeInterval):
    global TIME_INTERVAL
    TIME_INTERVAL = float(timeInterval)
    print("Changing time interval to", TIME_INTERVAL)

@eel.expose
def endTask(pid):
    try: 
        subprocess.run(["kill","-9",pid])
        print("Ending Task with PID:", pid)
    except:
        print("Error ending task ",pid)

def updateDataThread():
    try:
        while(True):
            eel.sleep(TIME_INTERVAL)

            """
            *********************************************************
            Memory Stats
            TYPES:
                memTotal:float
                memUsed:BasicGauge
                memUtil:float
            *********************************************************
            """
            memTotal, memUsed, memUtil = memStats.fetchAll()
            
            """
            eel.setMemoryTotal(round2(memTotal))
            eel.setMemoryAvailable(round2(memUsed.calculateAverage())) 
            eel.setMemoryUtilization(round2(memUtil))
            """
            eel.setMemoryStats([round2(memTotal), round2(memUsed.calculateAverage()), round2(memUtil)])
            


            """
            *********************************************************
            Disk Stats
            TYPES
                diskList:list of disk.Disk
            *********************************************************
            """
            diskList = diskStats.fetchAll()
            diskDictList = []
            for eachDisk in diskList:
                diskDictList.append(eachDisk.toJSON())   
 
            eel.setDiskStats(diskDictList)

            
            """
            *********************************************************
            Cpu Stats
            TYPES
                intr:BasicCounter
                ctxt:BasicCounter
                cpuList:list of cpu.Cpu
            *********************************************************
            """ 
            intr, ctxt, cpuList, _ = cpuStats.fetchAll() 
            eel.setIntr(round2(intr.calculateFrequencies()))
            eel.setCtxt(round2(ctxt.calculateFrequencies())) 
            
            cpuDictList = []
            for eachCpu in cpuList:
                cpuDictList.append(eachCpu.toJSON())   

            eel.setCpuStats(cpuDictList)


            """
            *********************************************************
            Process Stats
            TYPES
                processDict:dictionary of process.Process
            *********************************************************
            """
            processStats.setSysWideCpuTime(cpuStats.getSystemWideCpuTime())      
            processStats.setPhyMemTotal(int(memStats.getMemTotal()))
            processDictList = processStats.toJSON()   
            
            eel.setProcesses(processDictList)


            """
            *********************************************************
            Network Stats
            TYPES
                networkDeviceList:list of networkDevice.NetworkDevice
            *********************************************************
            """
            networkDeviceList = netStats.fetchAll()
            
            networkDictList = []
            for eachNetworkDevice in networkDeviceList:
                networkDictList.append(eachNetworkDevice.toJSON())   

            eel.setNetworkStats(networkDictList)


            """
            *********************************************************
            TCP/UDP Stats
            TYPES
                tcp:list of connection.Connection
                udp:list of connection.Connection
                establishedTcp:int
            *********************************************************
            """
            tcpUdpConnStats.updateInodeDict(processStats.getInodeDict())
            tcp, udp, establishedTcp = tcpUdpConnStats.fetchAll()
            
            tcpDictList = []
            for eachTcpConn in tcp:
                tcpDictList.append(eachTcpConn.toJSON())   

            eel.setTcpConnections(tcpDictList)

            udpDictList = []
            for eachUdpConn in udp:
                udpDictList.append(eachUdpConn.toJSON())   

            eel.setUdpConnections(udpDictList)

            eel.setEstTcp(establishedTcp, len(tcp))
        
    except KeyboardInterrupt:
        print("Closing")

@eel.expose
def toggleKeylogger(flag):
    print("Toggle Keylogger ", flag)
    global KEYLOGGER_ON
    if flag:
        try:
            subprocess.run(["sudo","insmod","./driver/intrpt.ko"])
            KEYLOGGER_ON= flag
            print("Turning on Keylogger")
        except:
            print("Error with insmod")

        try:
            eel.spawn(keyloggerThread)
        except:
            print("Error spawning keylogger thread")
    else:
        try:
            subprocess.run(["sudo","rmmod","intrpt"])
            KEYLOGGER_ON = flag
            
            print("Turning off Keylogger")
        except:
            print("Error with rmmod")
            

def keyloggerThread(): 
    """
    *********************************************************
    Keylogger 
    *********************************************************
    """  
    try:
        global KEYLOGGER_ON
        while(KEYLOGGER_ON): 
            try:
                logFile = readFile("/proc/keylogger") 
                date = logFile[0:10]
                time = logFile[11:19]
                content = logFile[20:]
                if(content):
                    print(content)
            
                eel.setLoggerData([date, time, content])
            except:
                print("Error in keylogger fetching")
            eel.sleep(1)
    except KeyboardInterrupt:
        print("Closing keylogger")


eel.spawn(updateDataThread)

print("On browser navigate to : localhost:8000/main.html") 
eel.start('main.html', mode="False") 


