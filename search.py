import datetime
import time
import csv
import os, glob
import argparse
import sys


### GLOBALS ###

# Directorys and file extensions #
GPONDIRECTORY = 'GPON_CSV/'
CSVEXTENS = '.csv'


# This script will allow you to search through all of the historical data collected on customers bandwidth usage
class searchManager():

    def __init__(self):

        self.searchManager()



    def searchManager(self):
        self.filesList = []

        self.historicalListManager()

        self.appArgs()
        #self.searchHistorical()



    def appArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--name", help="Search for customer with name")
        parser.add_argument("--ont", help="Search for customer with ONT")
        parser.add_argument("--id", help="Search for customer with ID")
        parser.add_argument("--vlan", help="Search for customer with VLAN")
        args = parser.parse_args()

        if args.name:
            self.searchHistorical(args.name, 'name')
        if args.ont:
            self.searchHistorical(args.ont, 'ont')
        if args.id:
            self.searchHistorical(args.id, 'id')
        if args.vlan:
            self.searchHistorical(args.vlan, 'vlan')



    def searchHistorical(self, searchTxt, searchType):
        matches = []

        for x in self.historicalList:
            for o in x:

                # This should be more dynamic so we can search for more than one property at a time
                if searchType == 'name':
                    if o[9] == searchTxt: # Customer name
                        #print ('Name match.')
                        matches.append(o)
                if searchType == 'ont':
                    if o[10] == searchTxt: # ONT
                        #print ('ONT match.')
                        matches.append(o)
                if searchType == 'id':
                    if o[7] == searchTxt: # ID
                        #print ('ID match.')
                        matches.append(o)
                if searchType == 'vlan':
                    if o[2] == searchTxt:
                        #print ('VLAN match')
                        matches.append(o)

        if not matches:
            return

        print (matches[1])

        test = []

        timeStampsList = []
        for ma in range(0, len(matches)):
            timeList = []
            timeList.append(matches[ma][3])
            timeList.append(matches[ma][4])
            timeList.append(matches[ma][5])

            timeStampsList.append(timeList)

        test.append(matches[0][0])
        test.append(matches[0][1])
        test.append(matches[0][2])
        test.append(matches[0][6])
        test.append(matches[0][7])
        test.append(matches[0][8])
        test.append(matches[0][9])
        test.append(matches[0][10])

        test.append(timeStampsList)
        print (test)





    def historicalListManager(self):
        self.importCustomerData()

        self.historicalList = []

        for files in range (0, len(self.filesList)):
            filename = self.filesList[files]
            customerList = self.parseHistoricalCSV(filename)
            self.historicalList.append(customerList)

        #print (self.historicalList)



    # Find all files in directory and appends them to a list
    def importCustomerData(self):
        for root, dirs, files in os.walk(GPONDIRECTORY):
            for file in files:
                if file.endswith(CSVEXTENS):
                    self.filesList.append(GPONDIRECTORY + file) # Append file directory and name to a list



    # Reads CSV file and converts the rows into lists and puts them into a list
    def parseHistoricalCSV(self, csvFile):

        customerList = []

        with open(csvFile) as csvData:
            readCSV = csv.reader(csvData, delimiter = ',')

            for row in readCSV:
                if len(row) == 10: # This is to ignore the human readable header (Will be based on str match later)
                    continue

                csvList = []

                csvList.append(row[0])  # Index
                csvList.append(row[1])  # Portchannel
                csvList.append(row[2])  # VLAN
                csvList.append(row[3])  # In octet
                csvList.append(row[4])  # Out octet
                csvList.append(row[5])  # Timestamp
                csvList.append(row[6])  # Network
                csvList.append(row[7])  # ID
                csvList.append(row[8])  # Match
                csvList.append(row[9])  # Description
                csvList.append(row[10]) # ONT

                customerList.append(csvList)

        # Close the GPON csv file
        csvData.close()


        # TEMPORARY #
        TTest = []
        for x in customerList:
            TTest.append(x[9])

        #print (TTest)
        result = self.remove_duplicates(TTest)
        print(result)


        return customerList # Returns customer data from the CSV file as a list




    def remove_duplicates(self, values):
        output = []
        seen = set()
        for value in values:
            # If value has not been encountered yet,
            # ... add it to both list and set.
            if value not in seen:

                output.append(value)
                seen.add(value)
        print (seen)
        return output


searchManager()