import time
import memStats
import diskStats
import cpuStats
import processStats
import netStats
import tcpUdpConnStats

TIME_INTERVAL = None

#TIME_INTERVAL = 1

while not TIME_INTERVAL:
    try:
        TIME_INTERVAL = int(input("What time interval would you like to use?(in sec) "))
    except:
        print("Please enter a valid time interval.")

try:
    while(True):
        time.sleep(TIME_INTERVAL)
        
        print("\nMEMORY:")
        memStats.printAll()
       
        print("\nDisk:")
        diskStats.printAll()
        
        print("\nCPU:")
        cpuStats.printAll() 
        
        print("\nProcess:")
        processStats.setSysWideCpuTime(cpuStats.getSystemWideCpuTime())        
        processStats.setPhyMemTotal(int(memStats.getMemTotal()))
        processStats.printAll() 

        print("\nNetwork:")
        netStats.printAll()
        
        print("\nTCP & UDP Connection:")
        tcpUdpConnStats.updateInodeDict(processStats.getInodeDict())
        tcpUdpConnStats.printAll()
        print("\n-----------------------------\n")
except KeyboardInterrupt:
    print("\nexiting...")
