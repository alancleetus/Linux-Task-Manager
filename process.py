from helperFunctions import round2
class Process:
    def __init__(self, pid):
        self.pid = pid
        self.name = ""
        self.userName = ""
        self.inodeNumber = ""
        self.userMode = {"prev":0, "curr":0}
        self.sysMode = {"prev":0, "curr":0}
        self.vmem = {"prev":0, "curr":0}
        self.rss = {"prev":0, "curr":0}
        self.time = {"prev":0, "curr":0}

    def updateName(self, name): 
        self.name = name 

    def updateUserName(self, userName):
        self.userName = userName 
    
    def updateInodeNumber(self, inodeNumber):
        self.inodeNumber = inodeNumber 
    
    def updateUserMode(self, userMode):
        self.userMode["prev"] = self.userMode["curr"]
        self.userMode["curr"] = userMode 

    def updateSysMode(self, sysMode):
        self.sysMode["prev"] = self.sysMode["curr"]
        self.sysMode["curr"] = sysMode 

    def updateVmem(self, vmem):
        self.vmem["prev"] = self.vmem["curr"]
        self.vmem["curr"] = vmem 
    
    def updateRss(self, rss):
        self.rss["prev"] = self.rss["curr"]
        self.rss["curr"] = rss 

    def updateTime(self, time):
        self.time["prev"] = self.time["curr"]
        self.time["curr"] = time 

    def updateAll(self, name, userName, inodeNumber, userMode, sysMode, vmem, rss, time):
        self.updateName(name)
        self.updateUserName(userName)        
        self.updateInodeNumber(inodeNumber)
        self.updateUserMode(userMode)
        self.updateSysMode(sysMode)        
        self.updateVmem(vmem)    
        self.updateRss(rss)
        self.updateTime(time)

    def calculateCpuUtilization(self, sysWidetime):
        
        delta_userMode = int(self.userMode["curr"]) - int(self.userMode["prev"])
        delta_sysMode = int(self.sysMode["curr"]) - int(self.sysMode["prev"])

        userModeUtil = 0
        sysModeUtil = 0
        totalUtil = 0
        try:
            userModeUtil = (delta_userMode/sysWidetime)*100
            sysModeUtil = (delta_sysMode/sysWidetime)*100
            totalUtil = ((delta_sysMode+delta_userMode)/sysWidetime) *100
        except ZeroDivisionError:
            pass

        return {"userMode":round2(userModeUtil), "sysMode":round2(sysModeUtil),"total":round2(totalUtil)}

    def calculateVmemUtil(self, vMemTotal):
        try:
            #delta_vmem = int(self.vmem["curr"]) - int(self.vmem["prev"]) 
            delta_vmem = int(self.vmem["curr"])
            totalUtil = (delta_vmem/int(vMemTotal))*100    
            #print(delta_vmem, vMemTotal, totalUtil)     
            return round2(totalUtil)
        except:
            #print("Error calculation vmem", vMemTotal, self.vmem)
            return 0

    def calculatePhyMemUtil(self, phyMemTotal):
        try:    
            #delta_phyMem = int(self.rss["curr"]) - int(self.rss["prev"]) 
            delta_phyMem = int(self.rss["curr"])
            totalUtil = (delta_phyMem/int(phyMemTotal))*100
            return round2(totalUtil)
        except:
            return 0

    def __eq__(self, other): 
        if not isinstance(other, Process):
            return NotImplemented

        return self.pid == other.pid

    def __str__(self):
        msg = "PID: {}\n Name: {}\n UserName: {}\n inodeNumber: {}\n User Mode:\tprev:{}\tcurr:{}\n Sys Mode:\tprev:{}\tcurr:{}\n Vmem Size:\tprev:{}\tcurr:{}\n Rss:\tprev:{}\tcurr:{}\n Time:\tprev:{}\tcurr:{}\n".format(
            self.pid, 
            self.name, 
            self.userName, 
            self.inodeNumber,
            self.userMode["prev"],
            self.userMode["curr"],
            self.sysMode["prev"],
            self.sysMode["curr"],
            self.vmem["prev"],
            self.vmem["curr"],
            self.rss["prev"],
            self.rss["curr"],
            round2(self.time["prev"]),
            round2(self.time["curr"])  
        )

        return msg

    def __repr__(self):
        return str(self)