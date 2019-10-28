import eel
import memStats
import diskStats
import cpuStats
import processStats
import netStats
import tcpUdpConnStats
from helperFunctions import round2

eel.init('web')

TIME_INTERVAL = 1

@eel.expose
def setTimeInterval(timeInterval):
    global TIME_INTERVAL
    TIME_INTERVAL = float(timeInterval)

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
            eel.setMemoryTotal(round2(memTotal))
            eel.setMemoryAvailable(round2(memUsed.calculateAverage())) 
            eel.setMemoryUtilization(round2(memUtil))


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

            #eel.consoleLog(cpuDictList)


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


eel.spawn(updateDataThread)
myOptions = {'size': (600, 400), "block": "False", "mode":"firefox"}

eel.start('main.html')
