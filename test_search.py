import subprocess
import argparse
import datetime
import os

import matplotlib.pyplot as plt
import numpy as np

from graphing import graphingManager


### GLOBALS ###

# Directorys and file extensions #
GPONDIRECTORY = 'CUSTOMER_DATA_CSV/'
CSVEXTENS = '.csv'
TEMPFILE = 'temp.txt'

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



        self.argsManager()



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

                #print (n)

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

            #print ("?")
            #print (n[0])
            #print (cIndex)

            # Make sure we only retrive the data from a single customer
            if n[0] == cIndex: # This statement is to make sure we only put the octet data of a single customer in the output.
                # Octet data #
                octetListSingle = [] # List for AN individual in and out octet w/ timestamp
                octetListSingle.append(n[3])  # In octet
                octetListSingle.append(n[4])  # Out octet
                octetListSingle.append(n[5])  # Timestamp

                #dTime = datetime.datetime.fromtimestamp(float(n[5])).strftime('%c')
                #octetListSingle.append(dTime)  # Timestamp

                octetListTotal.append(octetListSingle) # Append an octet single, to the octet total list

            self.nameCollision(cIndex, n[0]) # IF WE HAVE A REPEAT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        customerList.append(octetListTotal) # Append the total octet list to the customer list

        #print (customerList)
        with plt.style.context('ggplot'):
            #self.graph(customerList)
            self.graphPrerequisites(customerList)



    def nameCollision(self, staticIndex, customerIndex):
        if customerIndex != staticIndex:
            print ("This customer has the same value as another, search using different criteria.")
            print ("Index value of customer A: " + customerIndex)
            print ("Index value of customer B: " + staticIndex)



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
        self.grepCommand(name)
        self.grepParser()



    def graph(self, customerList):

        outUsage = []
        timeL = []

        timeSeconds = []

        firstSample = True

        for uu in customerList[10]:
            outOctet = (int(uu[1]))
            outOctet = self.octetToMb(outOctet)
            time = (float(uu[2]))

            outUsage.append(outOctet)

            if not firstSample:
                # Visual data
                timeStr = datetime.datetime.fromtimestamp(time).strftime('%H:%M')
                timeL.append(timeStr)

            # Seconds
            timeSeconds.append(time)

            firstSample = False



        outUsageDiff = [outUsage[i + 1] - outUsage[i] for i in range(len(outUsage) - 1)]
        timeDiff = [timeSeconds[i + 1] - timeSeconds[i] for i in range(len(timeSeconds) - 1)]


        #print (outUsageDiff)

        sortedUsageDiff = sorted(outUsageDiff)
        length = len(sortedUsageDiff)


        calcC = round((length * 0.95))

        #print (sortedUsageDiff[calcC])
        #print (sortedUsageDiff)




        bpsList = []
        count = len(outUsageDiff)


        for x in range(0, count):
            dataSample = outUsageDiff[x]
            timePeriod = timeDiff[x]

            bitsPerSec = dataSample / timePeriod

            bpsList.append(bitsPerSec)


        #print (timeL)

        plt.autoscale(enable=True, axis='both', tight=None)
        fig, ax = plt.subplots(nrows=1, ncols=1)  # create figure & 1 axis
        fig.set_size_inches(20, 10.0, forward=True)

        plt.ylabel('Log of Bits Per Second')
        plt.xlabel('Time')



        #ax.plot(timeL, bpsList, marker='o', markevery=9)
        ax.plot(timeL, bpsList)

        locs, labels = plt.xticks()
        labelList = self.removeEveryOther(locs)


        plt.xticks(labelList)

        fig.savefig('graph_usage.png')  # save the figure to file
        plt.close(fig)  # close the figure



    def removeEveryOther(self, my_list):
        length = len(my_list)

        cut = 1

        if length > 50:
            cut = 4

        if length > 100:
            cut = 8

        if length > 200:
            cut = 9

        if length > 300:
            cut = 11

        if length > 400:
            cut = 14

        if length > 600:
            cut = 30

        return my_list[::cut]



    def octetToMb(self, octet):
        mb = int(octet / 1048576) # Conversion from octet to Mb, converted to integer, strips anything after decimal
        return mb



    # Searches through all saved customer date using grep, and exports it to a temp file which is used later
    def grepCommand(self, name):
        command = "fgrep -h '%s' CUSTOMER_DATA_CSV/* > %s" % (name, TEMPFILE)
        subprocess.call(command, shell=True)



searchManager()


