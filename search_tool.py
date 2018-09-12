import matplotlib
matplotlib.use('Agg')

import subprocess
import argparse
import datetime
import bitmath
import yaml
import csv
import os

import matplotlib.pyplot as plt
import numpy as np

from graphing import graphingManager

### GLOBALS ###

# Directorys #
DATABASEFOLDER = 'Customer_Database/'
TEMPFILE = 'temp.txt'

# Config file locations #
CONFIGFOLDER = 'config/'
SERVICECONFIG = 'services.yaml'

# SEARCH ARGS #
SEARNAME = '--name'
SEARVLAN = '--vlan'
SEARONT = '--ont'
SEARID = '--id'
SEARINDEX = '--index'



# This script will allow you to search through all of the historical data collected on customers bandwidth usage
class searchManager(graphingManager):

    def __init__(self):
        print ("Grep searcher...")

        # Service type dictionary
        self.SERVICES = self.openYAML(CONFIGFOLDER + SERVICECONFIG)  # Reads YAML config file for available packages

        self.argsManager()



    def argsManager(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(SEARNAME, help="Search for customer with name") # Later on will require more than just customer info
        parser.add_argument(SEARVLAN, help="Search for customer with VLAN tag")
        parser.add_argument(SEARONT, help="Search for customer with ONT")
        parser.add_argument(SEARID, help="Search for customer with ID")
        parser.add_argument(SEARINDEX, help="Search for customer with ASR index value")
        args = parser.parse_args()

        self.searchSwitch(args)



    # Simple switch for the type of data user is searching for
    def searchSwitch(self, inputArgs):
        if inputArgs.name:
            self.searchCustomers(inputArgs.name)
        if inputArgs.vlan:
            self.searchCustomers(inputArgs.vlan)
        if inputArgs.ont:
            self.searchCustomers(inputArgs.ont)
        if inputArgs.id:
            self.searchCustomers(inputArgs.id)
        if inputArgs.index:
            self.searchCustomers(inputArgs.index)
        # Add new search fields here



    def searchCustomers(self, name):
        command = "fgrep -h '%s' %s* > %s" % (name, DATABASEFOLDER, TEMPFILE) # Searches through all saved customer date using grep, and exports it to a temp file which is used later
        self.externalProcess(command) # Run the command
        self.grepParser()



    def grepParser(self):
        with open(TEMPFILE, "r") as ins: # Opens the temp text file containing the grepped data
            lineArray = []
            for line in ins:
                lineArray.append(line.split('\n')[0])

        if lineArray == []:
            print ("Nothing found.")
            return

        # Vars
        customerList = [] # Single customer is appended in here, static data goes here
        octetListTotal = [] # Total octet list, this is where dynamic data goes
        staticFlag = 0 # Flag indicates if we've already appended static data
        maxUsageOut = 0

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

                # 3 thru 5 done later

                customerList.append(n[6])  # Region
                customerList.append(n[7])  # Service package
                customerList.append(n[8])  # ID
                customerList.append(n[9])  # Description
                customerList.append(n[10]) # ONT
                customerList.append(n[11]) # Ip Address
                customerList.append(n[12]) # Mac Address

            # Make sure we only retrive the data from a single customer
            if n[0] == cIndex: # This statement is to make sure we only put the octet data of a single customer in the output.
                # Octet data #
                octetListSingle = [] # List for AN individual in and out octet w/ timestamp

                octetListSingle.append(n[3])  # In octet
                octetListSingle.append(n[4])  # Out octet
                octetListSingle.append(n[5])  # Timestamp

                octetListTotal.append(octetListSingle) # Append an octet single, to the octet total list

            self.nameCollision(cIndex, n[0]) # IF WE HAVE A REPEAT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        customerList.append(octetListTotal) # Append the total octet list to the customer list

        self.other(customerList)

        self.tempFileCleanup()

        

    def other(self, customerList):

        graphList, bpsList, timeList = self.graphDataFormatter(customerList)

        maxPeak = max(bpsList)

        customerList.pop(10)
        customerList.append(maxPeak)
        #customerList.append(bpsList)
        #customerList.append(timeList)

        print (customerList)
        self.exportCustomer(customerList, bpsList, timeList)
        self.graphManager(graphList)



    def exportCustomer(self, customerList, bpsList, timeList):
        with open('test.csv', 'w') as csvCustomer:
            writeCSV = csv.writer(csvCustomer)

            writeCSV.writerow(customerList)

            tmp = []

            for x in range(0, len(bpsList)):
                t = []
                t.append(str(bpsList[x]))
                t.append(str(timeList[x]))
                tmp.append(t)
            print (tmp)

            writeCSV.writerow(tmp)



    def nameCollision(self, staticIndex, customerIndex):
        if customerIndex != staticIndex:
            print ("This customer has the same value as another, search using different criteria.")
            print ("Index value of customer A: " + customerIndex)
            print ("Index value of customer B: " + staticIndex)



    # Formats our data for exporting it to a visual graph.
    def graphDataFormatter(self, customerList):
        graphFormatList = []
        timeSeconds = []
        outUsage = []
        timeList = []
        firstSample = True

        serviceType = customerList[4]
        customerName = customerList[6]
        region = customerList[3]
        vlan = customerList[2]
        package = customerList[4]

        serviceUpDown = self.serviceToMaxUpDwn(serviceType)

        for uu in customerList[10]:
            outOctet = (int(uu[1]))
            time = (float(uu[2]))

            outUsage.append(outOctet)

            if not firstSample:
                # Visual data, this is what we draw on the png file for the time scale
                timeStr = datetime.datetime.fromtimestamp(time).strftime('%m/%d %H:%M')
                timeList.append(timeStr)

            timeSeconds.append(time) # Seconds
            firstSample = False

        outUsageDiff = [outUsage[i + 1] - outUsage[i] for i in range(len(outUsage) - 1)]
        timeDiff = [timeSeconds[i + 1] - timeSeconds[i] for i in range(len(timeSeconds) - 1)]

        count = len(outUsageDiff)
        bpsList = self.calculateBPS(count, outUsageDiff, timeDiff)  # Calls function
        peakDownload = max(bpsList)

        # This is all for the visual side of the graph
        graphFormatList.append(timeList)
        graphFormatList.append(bpsList)
        graphFormatList.append(serviceUpDown)
        graphFormatList.append(customerName)
        graphFormatList.append(region)
        graphFormatList.append(vlan)
        graphFormatList.append(package)

        return graphFormatList, bpsList, timeDiff # Reason we return multiple variables is that we will use bpsList and timeDiff when we export the specified customers' CSV



    def calculateBPS(self, count, usageDiff, timeDiff):
        bpsList = [] # Put our bits per second in list
        graphScale = 1000000

        for x in range(0, count):
            dataSample = usageDiff[x] * 8
            timePeriod = timeDiff[x]
            bitsPerSec = (dataSample / timePeriod)  / graphScale

            bpsList.append(bitsPerSec)

        return bpsList


        
    def octetToMb(self, octet):
        octetInt = int(octet)
        usageByte = bitmath.Byte(octetInt)
        usageMb = int(usageByte.to_MiB())

        return usageMb


        
    # Runs external bash commands
    def externalProcess(self, command):
        subprocess.call(command, shell=True)
        
        
     
    # Service to max download speeds list
    def serviceToMaxUpDwn(self, serviceType):
        maxUpDwn = self.SERVICES[serviceType] # Finds service's up and down speeds

        return maxUpDwn



    # Opens a yaml file and returns data stream
    def openYAML(self, filename):
        with open(filename, 'r') as stream:
            try:
                yamlDataFile = yaml.load(stream)
                return yamlDataFile
            except:
                    print (exc)
        
        
        
    def tempFileCleanup(self):
        # Delete no longer necessary temp files
        self.externalProcess("rm " + TEMPFILE)
    
    

searchManager()


