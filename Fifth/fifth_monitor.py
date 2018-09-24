import subprocess
import argparse
import datetime
import bitmath
import yaml
import csv
import os

import matplotlib.pyplot as plt
import numpy as np

### GLOBALS ###

DATABASEFOLDER = '../Customer_Database/'
MANUALFOLDER = '../CSV_Sources/' # Location of static data CSV files (Must be enerated with provided CSV tools)

STATICDATACSVAE = 'AE.csv'
STATICDATACSVGP = 'GPON.csv'

TEMPFILE = 'temp.txt'

PERCENTILETOCALCULATE = 95



# This tool is used to generate a list of all our customers with their percentiles
class percentileTool():

    def __init__(self):
        print ("Generating list of percentiles")

        self.allCustomers = []

        self.findAllCustomers()





    def findAllCustomers(self):
        self.allCustomerNames = []

        self.readGPCustomers()
        self.readAECustomers()

        for x in self.allCustomerNames:
            #print (x[0])
            #print (x[1])
            self.searchCustomers(x[0], x[1])



    def readGPCustomers(self):
        with open(MANUALFOLDER + STATICDATACSVGP) as csvGPON:
            readCSV = csv.reader(csvGPON, delimiter=',')

            for row in readCSV:
                oneCustomer = []

                customerName = (row[5])
                otag = (row[2])
                itag = (row[3])

                if len(itag) == 3: # Fix inTag by padding it with extra zero when neccessary
                    itag = '0' + str(itag)

                vlan = otag + itag

                oneCustomer.append(customerName)
                oneCustomer.append(vlan)
                self.allCustomerNames.append(oneCustomer)

        csvGPON.close()



    def readAECustomers(self):
        with open(MANUALFOLDER + STATICDATACSVAE) as csvAE:
            readCSV = csv.reader(csvAE, delimiter=',')

            for row in readCSV:
                oneCustomer = []

                customerName = (row[5])
                otag = (row[2])
                itag = (row[3])

                if len(itag) == 3: # Fix inTag by padding it with extra zero when neccessary
                    itag = '0' + str(itag)

                vlan = otag + itag

                oneCustomer.append(customerName)
                oneCustomer.append(vlan)
                self.allCustomerNames.append(oneCustomer)

        csvAE.close()



    def searchCustomers(self, name, vlan):
        command = 'fgrep -h "%s" %s* | fgrep -h "%s" > %s' % (name, DATABASEFOLDER, vlan, TEMPFILE) # Searches through all saved customer date using grep, and exports it to a temp file which is used later
        self.externalProcess(command) # Run the command
        self.grepParser()
        self.exportCustomers()



    def grepParser(self):
        with open(TEMPFILE, "r") as ins:  # Opens the temp text file containing the grepped data
            lineArray = []
            for line in ins:
                lineArray.append(line.split('\n')[0])

        if lineArray == []:
            #print ("Nothing found.")
            self.tempFileCleanup()
            return

        # Vars
        customerList = []  # Single customer is appended in here, static data goes here
        octetListTotal = []  # Total octet list, this is where dynamic data goes
        staticFlag = 0  # Flag indicates if we've already appended static data
        maxUsageOut = 0

        for lines in lineArray:  # Iterate over every line in the temp.txt file
            n = lines.split(",")  # Split every line into a list delimited by commas

            if staticFlag == 0:  # This is so we don't put the static information about the customer only once
                staticFlag = 1  # This flag indicates we have already appended the static customer data

                # This is so we can make sure we don't accidently get two different customers
                cIndex = n[0]
                cONT = n[10]

                customerList.append(n[0])  # ASR Index
                customerList.append(n[1])  # Porthchannel
                customerList.append(n[2])  # VLAN

                # 3 thru 5 done later

                customerList.append(n[6])  # Region
                customerList.append(n[7])  # Service package
                customerList.append(n[8])  # Description
                customerList.append(n[9])  # ONT
                customerList.append(n[10])  # Ip Address
                customerList.append(n[11])  # Mac Address

            # Make sure we only retrive the data from a single customer
            if n[0] == cIndex:  # This statement is to make sure we only put the octet data of a single customer in the output.
                # Octet data #
                octetListSingle = []  # List for AN individual in and out octet w/ timestamp

                octetListSingle.append(n[3])  # In octet
                octetListSingle.append(n[4])  # Out octet
                octetListSingle.append(n[5])  # Timestamp

                octetListTotal.append(octetListSingle)  # Append an octet single, to the octet total list

            self.nameCollision(cIndex, n[0])  # IF WE HAVE A REPEAT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        customerList.append(octetListTotal)  # Append the total octet list to the customer list

        self.extraData(customerList)




    def extraData(self, customerList):
        graphList, bpsList, timeList = self.graphDataFormatter(customerList)
        customerList.pop(9)

        maxPeak = max(bpsList)
        customerList.append(maxPeak)

        ourPercentile = self.calculatePercentile(bpsList)
        customerList.append(ourPercentile)

        self.allCustomers.append(customerList)



    def exportCustomers(self):
        with open('percentiles.csv', 'w') as csvfile:
            targetReader = csv.writer(csvfile, delimiter=',')

            for customerL in self.allCustomers:
                targetReader.writerow(customerL)
        csvfile.close()



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

        for uu in customerList[9]:
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



    # Service to max download speeds list
    def serviceToMaxUpDwn(self, serviceType):
        maxUpDwn = [50, 50] # Finds service's up and down speeds

        return maxUpDwn



    def nameCollision(self, staticIndex, customerIndex):
        if customerIndex != staticIndex:
            print ("This customer has the same value as another, search using different criteria.")
            print ("Index value of customer A: " + customerIndex)
            print ("Index value of customer B: " + staticIndex)



    def octetToMb(self, octet):
        octetInt = int(octet)
        usageByte = bitmath.Byte(octetInt)
        usageMb = int(usageByte.to_MiB())

        return usageMb



    def calculateBPS(self, count, usageDiff, timeDiff):
        bpsList = [] # Put our bits per second in list
        graphScale = 1000000

        for x in range(0, count):
            dataSample = usageDiff[x] * 8
            timePeriod = timeDiff[x]

            try: # Incase we divide by zero, we will ignore it and just set the BPS to zero.
                bitsPerSec = (dataSample / timePeriod)  / graphScale
            except:
                bitsPerSec = 0.0

            bpsList.append(bitsPerSec)

        return bpsList



    def calculatePercentile(self, bpsList):

        bpsArray = np.array(bpsList)
        thePercentile = np.percentile(bpsArray, PERCENTILETOCALCULATE)

        return thePercentile


    def tempFileCleanup(self):
        # Delete no longer necessary temp files
        self.externalProcess("rm " + TEMPFILE)



    # Runs external bash commands
    def externalProcess(self, command):
        subprocess.call(command, shell=True)



percentileTool()


