import json
from helperFunctions import round2
class NetworkDevice:
    def __init__(self, name):
        self.name = name
        self.bytesIn = {"prev": 0, "curr": 0}
        self.bytesOut = {"prev": 0, "curr": 0}
        self.networkBandwidth = {"prev": 0, "curr": 0}
        self.time = {"prev": 0, "curr": 0}

    def updateBytesIn(self, bytesIn):
        self.bytesIn["prev"] = self.bytesIn["curr"]
        self.bytesIn["curr"] = bytesIn

    def updateBytesOut(self, bytesOut):
        self.bytesOut["prev"] = self.bytesOut["curr"]
        self.bytesOut["curr"] = bytesOut

    def updateNetworkBandwidth(self, networkBandwidth):
        self.networkBandwidth["prev"] = self.networkBandwidth["curr"]
        self.networkBandwidth["curr"] = networkBandwidth

    def updateTime(self, time):
        self.time["prev"] = self.time["curr"]
        self.time["curr"] = time

    def updateAll(self, bytesIn, bytesOut, networkBandwidth, time):
        self.updateBytesIn(bytesIn)
        self.updateBytesOut(bytesOut)
        self.updateNetworkBandwidth(networkBandwidth)
        self.updateTime(time)

    def calculateDelta(self, dictItem):
        return float(dictItem["curr"]-dictItem["prev"])

    def calculateAverage(self, dictItem):
        return float(dictItem["curr"]+dictItem["prev"])/2

    def calculateUtilizationPerSecond(self):
        try:
            if self.networkBandwidth["prev"] == 0:
                return 0

            timeInterval = self.calculateDelta(self.time)
            bytesInPerSec = (self.calculateDelta(self.bytesIn)) / timeInterval
            bytesOutPerSec = (self.calculateDelta(self.bytesOut)) / timeInterval
            #print("Calc:", timeInterval, bytesInPerSec, bytesOutPerSec, self.calculateAverage(self.networkBandwidth))
            utilPerSec = (bytesInPerSec+bytesOutPerSec)/self.calculateAverage(self.networkBandwidth)
            return utilPerSec* 100
        except:
            print("Error calculating network utilization per second")
            return 0

    def __eq__(self, other):
        if not isinstance(other, NetworkDevice):
            return NotImplemented

        return self.name == other.name

    def __str__(self):

        msg = "Name: {}\n Bytes in\tprev:{}\tcurr:{}\n Bytes out\tprev:{}\tcurr:{}\n Network Bandwidth\tprev:{}\tcurr:{}\n Utilization:\t{}% per sec\n Read Time\tprev:{}\tcurr:{}\n".format(
            self.name,
            self.bytesIn["prev"],
            self.bytesIn["curr"],
            self.bytesOut["prev"],
            self.bytesOut["curr"],
            self.networkBandwidth["prev"],
            self.networkBandwidth["curr"],
            round2(self.calculateUtilizationPerSecond()),
            round2(self.time["prev"]),
            round2(self.time["curr"])
        )

        return msg

    def __repr__(self):
        return str(self)
       
    def toJSON(self): 
        data = {}
        data['name'] = self.name
        data['bytesIn'] = round2(self.calculateDelta(self.bytesIn))
        data['bytesOut'] = round2(self.calculateDelta(self.bytesOut))
        data['networkBandwidth'] = round2(self.calculateAverage(self.networkBandwidth))
        data['networkUtilization'] = round2(self.calculateUtilizationPerSecond())
        
        json_data = json.dumps(data)
        return json_data