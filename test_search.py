import subprocess
import os

### GLOBALS ###

# Directorys and file extensions #
GPONDIRECTORY = 'GPON_CSV/'
CSVEXTENS = '.csv'

TEMPFILE = 'temp.txt'


# This script will allow you to search through all of the historical data collected on customers bandwidth usage
class searchManager():

    def __init__(self):
        print ("Grep searcher...")

        self.grepCommand("fgrep -h 'Tosha Brooks' GPON_CSV/* > temp.txt")

        self.grepParser()



    def grepCommand(self, command):
        subprocess.call(command, shell=True)



    def grepParser(self):
        with open(TEMPFILE, "r") as ins: # Opens the temp text file containing the grepped data
            lineArray = []
            for line in ins:
                lineArray.append(line.split('\n')[0])

        # Vars
        customerList = [] # Single customer is appended in here, static data goes here
        octetListTotal = [] # Total octet list, this is where dynamic data goes
        staticFlag = 0 # Flag indicates if we've already appended static data
        
        for lines in lineArray: # Iterate over every line in the temp.txt file
            n = lines.split(",") # Split every line into a list delimited by commas
            
            if staticFlag == 0: # This is so we don't put the static information about the customer only once
                staticFlag = 1 # This flag indicates we have already appended the static customer data
                customerList.append(n[0])  # ASR Index
                customerList.append(n[1])  # Porthchannel
                customerList.append(n[2])  # VLAN
                customerList.append(n[6])  # Network
                customerList.append(n[7])  # ID
                customerList.append(n[8])  # MATCH
                customerList.append(n[9])  # Description
                customerList.append(n[10]) # ONT

            # Octet data #
            octetListSingle = [] # List for AN individual in and out octet w/ timestamp
            octetListSingle.append(n[3])  # In octet
            octetListSingle.append(n[4])  # Out octet
            octetListSingle.append(n[5])  # Timestamp
            octetListTotal.append(octetListSingle) # Append an octet single, to the octet total list
            
        customerList.append(octetListTotal) # Append the total octet list to the customer list

        print (customerList)
        
searchManager()


