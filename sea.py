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

        #self.combineHistOctets()



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
        print ("?")
        parser = argparse.ArgumentParser()
        parser.add_argument(SEARNAME, help="Search for customer with name") # Later on will require more than just customer info
        parser.add_argument(SEARONT, help="Search for customer with ONT")
        parser.add_argument(SEARID, help="Search for customer with ID")
        parser.add_argument(SEARINDEX, help="Search for customer with ASR index value")
        args = parser.parse_args()

        self.searchSwitch(args)


    # Simple switch for the type of data user is searching for
    def searchSwitch(self, inputArgs):
        print ("search")
        if inputArgs.name:
            self.searchName(inputArgs.name)
        if inputArgs.ont:
            self.searchONT(inputArgs.ont)
        if inputArgs.id:
            self.searchID(inputArgs.id)
        if inputArgs.index:
            self.searchIndex(inputArgs.vlan)
        # Add new search fields here



    # Search through historical lists for specific customer name
    def searchName(self, name):
        print ("search name")
        nameMatches = []

        for xList in self.historicalList: # xList is essentially an (individual) CSV file that has been converted to a list

            # Put check for customer's with same name HERE
            if not self.hasDuplicateNames(xList, name): # THIS IS MERGING THE CSV FILES, SO WE SHOULD CHECK WHAT THE INDEX VALUE IS
                return

            for customers in xList:

                if customers[9] == name:  # Name
                    # We have a name match.
                    nameMatches.append(customers)


        ###### Somewhere in here we need to deal with multiple people with the SAME name!!! ######

        self.combineHistOctets(nameMatches)


    # Search through historical lists for specific ONT
    def searchONT(self, ont):
        pass


    # Search through historical lists for specific ID
    def searchID(self, id):
        pass


    # Search through historical lists for index
    def searchIndex(self, index):
        pass



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
        print ("?")

        custCount = 0
        histCount = 0

        for x in self.historicalList:
            for y in self.historicalList[histCount]:

                #print (y)
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

            #print (z[0])

            for a in unsortedList:

                #### IMPORTANT ####
                if a[0] == custIndex and a[2] == custVlan and a[7] == custID: # This is to make sure we're combining the OCTETS of the same customer, can be easily modified.

                    # Append the different octet data




                    ##################
                    custCombine.append(a[6])  # Network
                    custCombine.append(a[7])  # ID
                    custCombine.append(a[8])  # Matc
                    custCombine.append(a[9])  # Description
                    custCombine.append(a[10]) # ONT

                    timeList = []
                    timeList.append(a[3]) # IN Octet
                    timeList.append(a[4]) # OUT Octet
                    timeList.append(a[5]) # Timestamp
                    custCombine.append(timeList)



                    #custCombine.append(a[7])


            combinedLists.append(custCombine) # Append this to our main list

        print (combinedLists)
        #print (combinedLists)

        #for d in combinedLists:
        #    print (d)


        #for cVar in range(0, len(self.historicalList)): # Dump all customers into one giant list

            #for customer in self.historicalList[cVar]:
            #    unsortedList.append(customer)

            #unsortedList.append(self.historicalList[cVar])


        #count = 0
        #for x in range(0, len(self.historicalList)):
            #count += 1

            #print (count)

            #print (test[0])



        #print (unsortedList[0])



searchManager()