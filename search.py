import datetime
import time
import csv
import os, glob


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

        self.searchHistorical()


    def searchHistorical(self):
        customerName = input('Customer name: ')

        matches = []

        for x in self.historicalList:
            for o in x:
                if o[9] == customerName:
                    print ('We have a match.')
                    matches.append(o) # Append the matching lists to " matches "

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

        test.append(timeStampsList)
        print (test)

    def historicalListManager(self):

        self.importCustomerData()

        self.historicalList = []

        for files in range (0, len(self.filesList)):
            filename = self.filesList[files]
            customerList = self.parseHistoricalCSV(filename)
            self.historicalList.append(customerList)

        print (self.historicalList)


    # Find all files in directory and appends them to a list
    def importCustomerData(self):
        for root, dirs, files in os.walk(GPONDIRECTORY):
            for file in files:
                if file.endswith(CSVEXTENS):
                    self.filesList.append(GPONDIRECTORY + file) # Append file directory and name to a list


    # Reads CSV file and converts the rows into lists and puts them into a list
    def parseHistoricalCSV(self, csvFile, ):

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

        return customerList # Returns customer data from the CSV file as a list

searchManager()