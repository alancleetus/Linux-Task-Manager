"""
In this module we calculate the network utilization for all network devices on this system.
"""
import re
from networkDevice import NetworkDevice
import subprocess
import time
from helperFunctions import readFile

lastReadTime = 0
networkBandwidths = {}
networkDeviceList = []

def getNetworkBandwidth(deviceName):
    global networkBandwidths
    try:
        if networkBandwidths[deviceName]:
            return networkBandwidths[deviceName]
    except:
        try:
            output = subprocess.check_output(["ethtool",deviceName]).decode("utf-8")
            speed = re.findall(r'Speed.*', output)[0].split()[1]
            bandwidth = re.sub(r'\D*','',speed)  #in Mb/s
            networkBandwidths[deviceName] = int(bandwidth)*125000 #Mb/s to Bytes/s

            print("Updating network bandwidth for",deviceName, "to", networkBandwidths[deviceName])
            return networkBandwidths[deviceName]
        except:
            print("Error: Unable to get network interface speed")
            return 0

def parseInfo(devFile, readTime):
    """
     This function takes the information from /proc/net/dev and parses it for relevant information.

     Parameters:
         devFile (str): The contents of /proc/net/dev.
         readTime (float): The time at which /proc/net/dev was read.
     Returns:
         list: Returns a list of NetworkDevice objects for each network device on the system.
     """
    global networkDeviceList
    try:
        for eachDev in devFile[2:-1]:
            #print(eachDev.split())
            deviceCols = eachDev.split()
            deviceName = deviceCols[0][:-1]

            if deviceName == "lo":
                continue

            try:
                index = networkDeviceList.index(NetworkDevice(str(deviceName)))
                networkDeviceList[index].updateAll(int(deviceCols[1]), int(deviceCols[8]), getNetworkBandwidth(deviceName), readTime)
            except:
                print("Adding new device", deviceName)
                temp_networkDevice = NetworkDevice(deviceName)
                print(temp_networkDevice)
                temp_networkDevice.updateAll(int(deviceCols[1]), int(deviceCols[8]), getNetworkBandwidth(deviceName), readTime)
                networkDeviceList.append(temp_networkDevice)

        return networkDeviceList

    except ZeroDivisionError:
        print("Error occurred while parsing /proc/net/dev file")
        return []


def fetchAll():
    readTime = time.time()
    devFile = readFile("/proc/net/dev").split("\n")
    return parseInfo(devFile, readTime)

def printAll():
    for dev in fetchAll():
        print(dev)

