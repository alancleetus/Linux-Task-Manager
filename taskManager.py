import time
import memStats
import diskStats
import cpuStats
import processStats
#import netStats
#import connStats

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
        
        print("\n-----------------------------\n")
except KeyboardInterrupt:
    print("\nexiting...")





















"""
try:
    while(True):
        time.sleep(TIME_INTERVAL)

       intr, ctxt, cpus = cpuStats.fetchAll()

        ####################  INTR & CTXT  ######################
        #print("\n{:=>100}".format(""))
        #print("intr: {}/sec \tctxt: {}/sec".format(intr, ctxt))

        ####################  CPU UTIL  ######################
        print("\nCPU Utilization:")
        print(" {:_>38}".format(""))
        print("|{:>5}|{:>10}|{:>10}|{:>10}|".format(
            "name", "stime(%)", "utime(%)", "total(%)"))
        print("|{:->5}|{:->10}|{:->10}|{:->10}|".format("", "", "", ""))
        for eachCpu in cpus:
            v = list(eachCpu.values())
            print("|{:>5}|{:>10.2f}|{:>10.2f}|{:>10.2f}|".format(
                v[0], v[1], v[2], v[3]))
        print(" {:=>38}".format(""))

        ####################  MEM UTIL  ######################
        print("\nMEMORY:")
        for k, v in memStats.fetchInfo().items():
            if k == "util":
                print(" {}: {}%".format(k, v))
            else:
                print(" {}: {} MB".format(k, v))

        ####################  DISK I/O ######################
        disks = diskStats.fetchAll()
        print("\nDISK:")
        for eachDisk in disks:
            for k, v in eachDisk.items():
                if k != "name":
                    print("  {}:{}/sec".format(k, v))
                else:
                    print(" {}".format(v))
     
        ####################  NETWORK  ####################
        #print(netStats.getNetInfo())


        ####################  CONNECTION  ####################
        tcp = netStats.getConnInfo("tcp")
        udp = netStats.getConnInfo("udp")
        tcpConnList = netStats.getConnInfo("tcp")
        udpConnList = netStats.getConnInfo("udp")


        print("\nTCP:\n{} current connections".format(len(tcpConnList)))
        netStats.printTable(tcpConnList)

        print("\nUDP:\n{} current connections".format(len(udpConnList)))
        netStats.printTable(udpConnList)
       
        ####################  PROSSESS  ####################
        procData = processStats.fetchAll()
        print(" {:_>96}".format(""))
        print("|{:>6}|{:>10}|{:>10}|{:>10}|{:>10}|{:>10}|{:>10}|{:>10}|{:>10}|".format(
            "pid", "User", "Program", "Utime", "Stime", "VSize", "PhySize", "VUtil", "PhyUtil"))
        print("|{:->6}|{:->10}|{:->10}|{:->10}|{:->10}|{:->10}|{:->10}|{:->10}|{:->10}|".format("","","", "", "", "", "", "", ""))
        for proc in procData: 
            print("|{:>6}|{:>10.10}|{:>10.10}|{:>10}|{:>10}|{:>10}|{:>10}|{:>10.2f}|{:>10.2f}|".format(
                proc[0], proc[1], proc[2], proc[3], proc[4], proc[5], proc[6], proc[7], proc[8]))
        print(" {:=>96}".format(""))

  
except KeyboardInterrupt:
    print("\nexiting...")
"""
