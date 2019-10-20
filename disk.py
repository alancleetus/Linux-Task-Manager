from helperFunctions import calculateCounterFreq, round2
class Disk:
    def __init__(self, name):
        self.name = name
        self.diskRead = {"prev":0, "curr":0}
        self.diskWrite = {"prev":0, "curr":0}
        self.blockRead = {"prev":0, "curr":0}
        self.blockWrite = {"prev":0, "curr":0}
        self.time = {"prev":0, "curr":0}

    def updateDiskRead(self, diskRead):
        self.diskRead["prev"] = self.diskRead["curr"]
        self.diskRead["curr"] = diskRead 

    def updateDiskWrite(self, diskWrite):
        self.diskWrite["prev"] = self.diskWrite["curr"]
        self.diskWrite["curr"] = diskWrite 

    def updateBlockRead(self, blockRead):
        self.blockRead["prev"] = self.blockRead["curr"]
        self.blockRead["curr"] = blockRead 

    def updateBlockWrite(self, blockWrite):
        self.blockWrite["prev"] = self.blockWrite["curr"]
        self.blockWrite["curr"] = blockWrite 

    def updateTime(self, time):
        self.time["prev"] = self.time["curr"]
        self.time["curr"] = time 

    def updateAll(self, diskRead, diskWrite, blockRead, blockWrite, time):
        self.updateDiskRead(diskRead)
        self.updateDiskWrite(diskWrite)
        self.updateBlockRead(blockRead)
        self.updateBlockWrite(blockWrite)
        self.updateTime(time)

    def calculateFrequencies(self):
        interval =  (self.time["curr"]-self.time["prev"])
        
        diskReadFreq = calculateCounterFreq(self.diskRead["prev"], self.diskRead["curr"], interval)

        diskWriteFreq = calculateCounterFreq(self.diskWrite["prev"], self.diskWrite["curr"], interval)

        blockReadFreq = calculateCounterFreq(self.blockRead["prev"], self.blockRead["curr"], interval)
        
        blockWriteFreq = calculateCounterFreq(self.blockWrite["prev"], self.blockWrite["curr"], interval)
     
        return {"diskRead":diskReadFreq, "diskWrite":diskWriteFreq,"blockRead":blockReadFreq, "blockWrite":blockWriteFreq}

    def __eq__(self, other): 
        if not isinstance(other, Disk):
            return NotImplemented

        return self.name == other.name

    def __str__(self):
        freqs = self.calculateFrequencies()

        msg = "Name: {}\n Disk Read\tprev:{}\tcurr:{}\tfreq:{}/s\n Disk Write\tprev:{}\tcurr:{}\tfreq:{}/s\n Block Read\tprev:{}\tcurr:{}\tfreq:{}/s\n Block Write\tprev:{}\tcurr:{}\tfreq:{}/s\n Read Time\tprev:{}\tcurr:{}\n".format(
            self.name, 
            self.diskRead["prev"],
            self.diskRead["curr"], 
            round2(freqs["diskRead"]),
            self.diskWrite["prev"],
            self.diskWrite["curr"], 
            round2(freqs["diskWrite"]),
            self.blockRead["prev"],
            self.blockRead["curr"], 
            round2(freqs["blockRead"]),
            self.blockWrite["prev"],
            self.blockWrite["curr"],
            round2(freqs["blockWrite"]),
            round2(self.time["prev"]),
            round2(self.time["curr"])          
        )

        return msg

    def __repr__(self):
        return str(self)