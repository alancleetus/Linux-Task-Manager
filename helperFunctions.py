"""
This is a helper module containing useful utility functions.  
"""

class BasicCounter: 
    def __init__(self, name):
        self.name = name
        self.count = {"prev":0, "curr":0}
        self.time = {"prev":0, "curr":0}

    def updateCount(self, count):
        self.count["prev"] = self.count["curr"]
        self.count["curr"] = count 

    def updateTime(self, time):
        self.time["prev"] = self.time["curr"]
        self.time["curr"] = time 

    def updateAll(self, count, time):
        self.updateCount(count) 
        self.updateTime(time)

    def calculateFrequencies(self):
        interval =  (self.time["curr"]-self.time["prev"])
        
        freq = calculateCounterFreq(self.count["prev"], self.count["curr"], interval)
 
        return freq

    def __eq__(self, other): 
        if not isinstance(other, BasicCounter):
            return NotImplemented

        return self.name == other.name

    def __str__(self):
        freq = self.calculateFrequencies()

        msg = "Name: {}\n Count\tprev:{}\tcurr:{}\tfreq:{}/s\n Read Time\tprev:{}\tcurr:{}\n".format(
            self.name, 
            self.count["prev"],
            self.count["curr"], 
            round2(freq),
            round2(self.time["prev"]),
            round2(self.time["curr"])          
        )

        return msg

    def __repr__(self):
        return str(self)


def readFile(path):
    """
    This function reads a file.

    This function takes in a valid path to a file that exists on the system and returns its contents as a string.  If the file does not exist then this function returns the keyword None

    Parameters: 
        path (str): A valid path to an existing file 
  
    Returns: 
        str: The contents of the file that is read or None
  
    """
    try:
        with open(path) as content:
            return content.read()
    except FileNotFoundError:
        print("FileNotFoundError in memStats.py: Invalid file path \"{}\"".format(path))
        return None

def round2(val):
    """
    This helper function rounds a real number to 2 decimal places.
    
    Parameters: 
        val (float): Real number to be rounder 
  
    Returns: 
        float: val but rounded to 2 decimal places or None if an error occurred
  
    """
    try:
        return round(val, 2)
    except:
        print("Error: Unable to round")
        return 0

def calculateCounterFreq(prev, curr, timeInterval):
    """
    This function calculates the frequency based on the current and previous values.

    Parameters:
        curr (float): The current value of a data set
        prev (float): The previous value of a data set
        timeInterval (float): The interval for which the frequency is calculated
    Returns:
        float: The calculated frequency
    """
    try:
        return (float(curr)-float(prev))/float(timeInterval) 
    except:
        print("Error: unable to calculate counter frequency. Values:\n curr:{} prev:{} interval:{}".format(curr, prev, timeInterval))
        return 0