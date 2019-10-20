"""
This is a helper module containing useful utility functions.  
"""

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
        return None

def calculateCounterFreq(prev, curr, timeInterval):
    """
    This function calculates the frequency based on the current and previous values.

    Parameters:
        curr (any number): The current value of a data set
        prev (any number): The previous value of a data set
        timeInterval (float): The interval for which the frequency is calculated
    Returns:
        float: The calculated frequency
    """
    try:
        return (curr-prev)/timeInterval 
    except:
        print("Error: unable to calculate counter frequency")
        return None