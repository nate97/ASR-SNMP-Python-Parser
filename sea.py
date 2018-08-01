import datetime
import time
import csv
import os, glob
import argparse
import sys
import collections

### GLOBALS ###

# Directorys and file extensions #
GPONDIRECTORY = 'GPON_CSV/'
CSVEXTENS = '.csv'

# SEARCH ARGS #
SEARNAME = '--name'
SEARONT = '--ont'
SEARID = '--id'
SEARINDEX = '--index'


# This script will allow you to search through all of the historical data collected on customers bandwidth usage
class searchManager():

    def __init__(self):

        self.historicalListManager()

        self.argsManager()



    # Calls all of the primary functions for EXTRACT THE CSV FILES, and defines their appropriate variables
    def historicalListManager(self):
        self.filesList = []
        self.historicalList = []
        self.comboHistorical = []

        self.importCustomerData()

        self.iterateCSVFiles()

        self.combineHistOctets()



    # Find all files in directory and appends them to a list
    def importCustomerData(self):
        for root, dirs, files in os.walk(GPONDIRECTORY):
            for file in files:
                if file.endswith(CSVEXTENS):
                    self.filesList.append(GPONDIRECTORY + file) # Append file directory and name to a list



    def parseHist(self, fileName):
        customerList = []

        with open(fileName) as csvData:
            readCSV = csv.reader(csvData, delimiter = ',')

            for row in readCSV:
                if row[0] == " INDEX": # This is to ignore the human readable header (Will be based on str match later)
                    continue

                customerRow = [] # Contains data from individual CSV line
                customerRow.append(row[0])  # Index
                customerRow.append(row[1])  # Portchannel
                customerRow.append(row[2])  # VLAN
                customerRow.append(row[3])  # In octet
                customerRow.append(row[4])  # Out octet
                customerRow.append(row[5])  # Timestamp
                customerRow.append(row[6])  # Network
                customerRow.append(row[7])  # ID
                customerRow.append(row[8])  # Match
                customerRow.append(row[9])  # Description
                customerRow.append(row[10]) # ONT

                customerList.append(customerRow)

        # Close the GPON csv file
        csvData.close()

        return customerList



    def iterateCSVFiles(self):
        for files in range (0, len(self.filesList)):
            filename = self.filesList[files]
            customerList = self.parseHist(filename)
            self.historicalList.append(customerList)



    def mergeHistCSV(self):
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
            self.searchName(inputArgs.name)
        if inputArgs.ont:
            self.searchONT(inputArgs.ont)
        if inputArgs.id:
            self.searchID(inputArgs.id)
        if inputArgs.index:
            self.searchIndex(inputArgs.index)
        # Add new search fields here



    # Search through historical lists for specific customer name
    def searchName(self, name):
        #print ("Searching for name: " + name)
        nameMatches = []

        for customer in self.comboHistorical: # xList is every customer we know about

            # Put check for customer's with same name HERE
            #if not self.hasDuplicateNames(xList, name): # THIS IS MERGING THE CSV FILES, SO WE SHOULD CHECK WHAT THE INDEX VALUE IS
            #    return

            if customer[6] == name:  # Name
                # We have a name match.
                nameMatches.append(customer)
                print (customer)



    # Search through historical lists for specific ONT
    def searchONT(self, ont):
        #print ("Searching for ONT: " + ont)
        ontMatches = []

        for customer in self.comboHistorical: # xList is every customer we know about

            if customer[7] == ont:  # ONT
                # We have a name match.
                ontMatches.append(customer)
                print (customer)



    # Search through historical lists for specific ID
    def searchID(self, id):
        #print ("Searching for ID: " + id)
        idMatches = []

        for customer in self.comboHistorical: # xList is every customer we know about

            if customer[4] == id:  # ID
                # We have a name match.
                idMatches.append(customer)
                print (customer)



    # Search through historical lists for index
    def searchIndex(self, index):
        #print ("Searching for index: " + index)
        indexMatches = []

        for customer in self.comboHistorical: # xList is every customer we know about

            if customer[0] == index:  # ID
                # We have a name match.
                indexMatches.append(customer)
                print (customer)



    def hasDuplicateNames(self, customerList, searchValue):
        identical = 0

        for customers in customerList:
            if searchValue in customers:
                if identical >= 1:
                    print ("ERROR: Identical names!")
                    continue

                identical =+1
                print ("OK")

        if identical >= 1:
            return False
        else:
            return True



    def combineHistOctets(self):
        unsortedList = []
        custCount = 0
        histCount = 0

        for x in self.historicalList:
            for y in self.historicalList[histCount]:

                unsortedList.append(y)
                custCount += 1 # Iterate over next customer

            histCount += 1 # Iterate over next set of customers


        combinedLists = []
        for z in unsortedList:
            custIndex = z[0] # ASR index value
            custVlan = z[2] # ASR customer vlan tag
            custID = z[7] # I'm using this incase we have an index value collision...
            custCombine = []


            # Only append these once.
            custCombine.append(custIndex) # Append ASR Index
            custCombine.append(z[1]) # Append portchannel
            custCombine.append(z[2]) # Append vlan tag

            ##################
            custCombine.append(z[6])  # Network
            custCombine.append(z[7])  # ID
            custCombine.append(z[8])  # Matc
            custCombine.append(z[9])  # Description
            custCombine.append(z[10])  # ONT

            for a in unsortedList:

                #### IMPORTANT ####
                if a[0] == custIndex and a[2] == custVlan and a[7] == custID: # This is to make sure we're combining the OCTETS of the same customer, can be easily modified.

                    # Append the different octet data

                    timeList = []
                    timeList.append(a[3]) # IN Octet
                    timeList.append(a[4]) # OUT Octet
                    timeList.append(a[5]) # Timestamp
                    custCombine.append(timeList)


            if custCombine not in self.comboHistorical: # Fixes issue where it would append identical copies of customers because of how we iterate through the unsorted list.
                self.comboHistorical.append(custCombine) # Append this to our main list
                #print (custCombine)



searchManager()