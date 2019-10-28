import re
import socket
import processStats
import pwd
from helperFunctions import readFile
from connection import Connection


ipDict = {}
userDict = {}
tcpConnList = []
udpConnList = []
inodeDict = {}

def convertIP(hexIP):
    """
    Convert ip in hex to string and return hostname if possible.

    :param hexIP: ip in hex
    :return: hostname of ip or the string ip value converted from hex
    """
    global ipDict
    if hexIP in ipDict.keys():
        return ipDict[hexIP]

    try:
        ip = socket.inet_ntoa(bytes.fromhex(hexIP))
        ipDict[hexIP] = socket.gethostbyaddr(ip)[0]
        return ipDict[hexIP]

    except socket.herror:
        ipDict[hexIP] = socket.inet_ntoa(bytes.fromhex(hexIP))
        print("Error: unable to resolve ip:",  socket.inet_ntoa(bytes.fromhex(hexIP)))
        return ipDict[hexIP]


def updateInodeDict(iDict):
    global inodeDict
    inodeDict = iDict


def getProgram(inode):
    global inodeDict
    try:
        pid = inodeDict[inode]
        if pid:
            #print("inode %s maps to pid %s" % (inode, pid))
            procFolderPath = "/proc/" + pid + "/comm"
            procFile = readFile(procFolderPath)
            program = procFile.strip()
            return program
    except:
        return ""

def parseInfo(connFile):
    connList = []

    try:
        for eachConn in connFile.split("\n")[1:-2]:
            eachConnCols = eachConn.split()
            id = eachConnCols[0][:-1]
            uid = int(eachConnCols[7])

            username = ""
            try:
                username = pwd.getpwuid(uid).pw_name
            except:
                print("Error getting username")

            inode = eachConnCols[9]

            program = ""
            try:
                program = getProgram(inode)
            except:
                print("Error getting program name")

            srcIp = eachConnCols[1].split(":")[0]
            srcHostName = convertIP(srcIp)
            srcPort = int(eachConnCols[1].split(":")[1], 16)
            destIp = eachConnCols[2].split(":")[0]
            destHostName = convertIP(destIp)
            destPort = int(eachConnCols[2].split(":")[1], 16)

            try:
                srcIp = socket.inet_ntoa(bytes.fromhex(srcIp))
            except:
                print("Error converting src ip")
            try:
                destIp = socket.inet_ntoa(bytes.fromhex(destIp))
            except:
                print("Error converting ip")

            src = {"hostname":srcHostName, "ip":srcIp, "port":srcPort}
            dest = {"hostname":destHostName, "ip":destIp, "port":destPort}

            temp_Conn = Connection(id)
            temp_Conn.updateAll(uid, username, inode,program,src,dest)
            connList.append(temp_Conn)

        return connList

    except:
        print("Error parsing file")
        return []

def countEstablished(tcpFile):
    try:
        count = 0
        for eachConn in tcpFile.split("\n")[1:-2]:
            eachConnCols = eachConn.split()
            connState = eachConnCols[0][:-1]
            if connState == "01":
                count+=1
        return count
    except:
        return 0

def fetchAll():
    global tcpConnList, udpConnList
    try:
        tcpFile = readFile("/proc/net/tcp")
        udpFile = readFile("/proc/net/udp")
        tcpConnList = parseInfo(tcpFile)
        udpConnList = parseInfo(udpFile)
        establishedTcpCount = countEstablished(tcpFile)
        return [tcpConnList, udpConnList, establishedTcpCount]
    except:
        print("Error fetching all")
        return []

def printAll():
    output = fetchAll()
    print("\nTcp:\n","Active Conn:", len(output[0]), "\tEstablished:",output[2])
    print("\n",output[0])
    print("\n",output[1])
