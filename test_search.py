import subprocess
import argparse
import os

### GLOBALS ###

# Directorys and file extensions #
GPONDIRECTORY = 'GPON_CSV/'
CSVEXTENS = '.csv'
TEMPFILE = 'temp.txt'

# SEARCH ARGS #
SEARNAME = '--name'
SEARONT = '--ont'
SEARID = '--id'
SEARINDEX = '--index'

# This script will allow you to search through all of the historical data collected on customers bandwidth usage
class searchManager():

    def __init__(self):
        print ("Grep searcher...")

        self.argsManager()



    def grepCommand(self, name):
        command = "fgrep -h '%s' GPON_CSV/* > %s" % (name, TEMPFILE)

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

                # This is so we can make sure we don't accidently get two different customers
                cIndex = n[0]
                cONT = n[10]

                customerList.append(n[0])  # ASR Index
                customerList.append(n[1])  # Porthchannel
                customerList.append(n[2])  # VLAN
                customerList.append(n[6])  # Network
                customerList.append(n[7])  # ID
                customerList.append(n[8])  # MATCH
                customerList.append(n[9])  # Description
                customerList.append(n[10]) # ONT
                customerList.append(n[11]) # PortChannel
                customerList.append(n[12]) # IP Address

            # Make sure we only retrive the data from a single customer
            if n[0] == cIndex: # This statement is to make sure we only put the octet data of a single customer in the output.
                # Octet data #
                octetListSingle = [] # List for AN individual in and out octet w/ timestamp
                octetListSingle.append(n[3])  # In octet
                octetListSingle.append(n[4])  # Out octet
                octetListSingle.append(n[5])  # Timestamp
                octetListTotal.append(octetListSingle) # Append an octet single, to the octet total list
            else:
                print ("This customer has the same value as another, search with different criteria for now")
                print ("This is the index value of omited customer: "+ n[0])


        customerList.append(octetListTotal) # Append the total octet list to the customer list

        print (customerList)



    def nameCollision(self):
        pass



    def argsManager(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(SEARNAME, help="Search for customer with name") # Later on will require more than just customer info
        parser.add_argument(SEARONT, help="Search for customer with ONT")
        parser.add_argument(SEARID, help="Search for customer with ID")
        parser.add_argument(SEARINDEX, help="Search for customer with ASR index value")
        args = parser.parse_args()

        self.searchSwitch(args)



    # Simple switch for the type of data user is searching for
    def searchSwitch(self, inputArgs):
        if inputArgs.name:
            self.searchCustomers(inputArgs.name)
        if inputArgs.ont:
            self.searchCustomers(inputArgs.ont)
        if inputArgs.id:
            self.searchCustomers(inputArgs.id)
        if inputArgs.index:
            self.searchCustomers(inputArgs.index)
        # Add new search fields here



    def searchCustomers(self, name):
        self.grepCommand(name)
        self.grepParser()



searchManager()


