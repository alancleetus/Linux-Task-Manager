from helperFunctions import calculateCounterFreq, round2
class Cpu:
    def __init__(self, name):
        self.name = name
        self.userMode = {"prev":0, "curr":0}
        self.sysMode = {"prev":0, "curr":0}
        self.idleMode = {"prev":0, "curr":0} 
        self.time = {"prev":0, "curr":0}

    def updateUserMode(self, userMode):
        self.userMode["prev"] = self.userMode["curr"]
        self.userMode["curr"] = userMode 

    def updateSysMode(self, sysMode):
        self.sysMode["prev"] = self.sysMode["curr"]
        self.sysMode["curr"] = sysMode 

    def updateIdleMode(self, idleMode):
        self.idleMode["prev"] = self.idleMode["curr"]
        self.idleMode["curr"] = idleMode 

    def updateTime(self, time):
        self.time["prev"] = self.time["curr"]
        self.time["curr"] = time 

    def updateAll(self, userMode, sysMode, idleMode, time):
        self.updateUserMode(userMode)
        self.updateSysMode(sysMode)
        self.updateIdleMode(idleMode)
        self.updateTime(time)

    def calculateUtilization(self):
        
        delta_userMode = int(self.userMode["curr"]) - int(self.userMode["prev"])
        delta_sysMode = int(self.sysMode["curr"]) - int(self.sysMode["prev"])
        delta_idleMode = int(self.idleMode["curr"]) - int(self.idleMode["prev"])

        sysWideTime = delta_idleMode + delta_sysMode + delta_userMode
        
        userModeUtil = (delta_userMode/sysWideTime)*100
        sysModeUtil = (delta_sysMode/sysWideTime)*100
        totalUtil = (delta_sysMode+delta_userMode)/sysWideTime *100
        
        return {"userMode":userModeUtil, "sysMode":sysModeUtil,"total":totalUtil}

    def __eq__(self, other): 
        if not isinstance(other, Cpu):
            return NotImplemented

        return self.name == other.name

    def __str__(self):
        util = self.calculateUtilization()

        msg = "Name: {}\n User Mode\tprev:{}\tcurr:{}\tutil:{}%\n Sys Mode\tprev:{}\tcurr:{}\tutil:{}%\n Idle Mode\tprev:{}\tcurr:{}\n total util:{}%\n Read Time\tprev:{}\tcurr:{}\n".format(
            self.name, 
            self.userMode["prev"],
            self.userMode["curr"], 
            round2(util["userMode"]),
            self.sysMode["prev"],
            self.sysMode["curr"], 
            round2(util["sysMode"]),
            self.idleMode["prev"],
            self.idleMode["curr"], 
            round2(util["total"]),
            round2(self.time["prev"]),
            round2(self.time["curr"])          
        )

        return msg

    def __repr__(self):
        return str(self)