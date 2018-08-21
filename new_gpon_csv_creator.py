import subprocess
import datetime
import time
import os
import csv

from collections import OrderedDict



class GponCombiner():

    def __init__(self):

        self.first()
        self.second()

        self.repeats()



    def first(self):
        self.externalProcess("awk 'NR>2' combine_gpon/gpon_ont_ge.csv > combine_gpon/gpon_ont_ge_nohead.csv")
        self.externalProcess('sort ' + 'combine_gpon/gpon_ont_ge_nohead.csv' +  ' > ' + 'combine_gpon/gpon_ont_ge_sorted.csv') # Sort
        self.gponGeList = self.iterateGeCSV('combine_gpon/gpon_ont_ge_sorted.csv')



    def second(self):
        self.externalProcess("awk 'NR>2' combine_gpon/gpon_data.csv > combine_gpon/gpon_data_nohead.csv")
        self.externalProcess('sort ' + 'combine_gpon/gpon_data_nohead.csv' +  ' > ' + 'combine_gpon/gpon_data_sorted.csv') # Sort
        self.gponDataList = self.iterateDataCSV('combine_gpon/gpon_data_sorted.csv')



    def lineIterator(self, filename):
        lineList = []
        fileA = open(filename, 'r')

        #for line in fileA.readlines():
            #print (line)
            #lineList.append(line)

        return lineList



    def iterateGeCSV(self, filename):
        with open(filename) as csvAE:
            readCSV = csv.reader(csvAE, delimiter=',')

            gponGeList = []

            for row in readCSV:
                region = row[0]
                descr = row[6]
                id = row[18]

                if descr == " ":
                    continue
                if region == " ":
                    continue
                if id == " ":
                    continue

                regionAndID = [region + ":" + id] # Create new individual column list
                row = regionAndID + row # Append new data to our row list
                gponGeList.append(row)

        csvAE.close()

        return gponGeList



    def iterateDataCSV(self, filename):
        with open(filename) as csvAE:
            readCSV = csv.reader(csvAE, delimiter=',')

            gponDataList = []

            for row in readCSV:
                region = row[0]
                descr = row[2]
                id = row[8]

                if region == " ":
                    continue
                if id == " ":
                    continue


                id = id.split("-GE")
                id = id[0]
                try:
                    id2 = id.split("-", 1)
                    correctedID = (id2[1])

                    regionAndID = [region + ":" + correctedID] # Create new individual column list
                    row = regionAndID + row # Append new data to our row list
                    gponDataList.append(row)

                except:
                    continue

        csvAE.close()

        return gponDataList



    def repeats(self):

        self.NEWgponGeList = self.remove_duplicates(self.gponGeList)

        self.NEWgponDataList = self.remove_duplicates(self.gponDataList)

        self.findMatch()



    def remove_duplicates(self, listy):
        newlist = [ii for n, ii in enumerate(listy) if ii not in listy[0][:n]]
        return newlist



    def findMatch(self):

        newCSVLines = []

        for GEGpon in self.NEWgponGeList:

            for GEData in self.NEWgponDataList:

                if GEGpon[0] in GEData[0]:

                    csvLine = []

                    #print (GEData)
                    #print (GEGpon)

                    """
                    print (GEData[1])  # Region
                    print (GEData[2])  # Network
                    print (GEData[3])  # Descr ( UNUSED )
                    print (GEData[4])  # TAG-ACTION
                    print (GEData[5])  # BW-PROF
                    print (GEData[6])  # OUT-TAG
                    print (GEData[7])  # IN-TAG
                    print (GEData[8])  # MCAST-PROF
                    print (GEData[9])  # ID

                    print (GEGpon[1])  # Region
                    print (GEGpon[2])  # Network
                    print (GEGpon[3])  # ID
                    print (GEGpon[4])  # intf
                    print (GEGpon[5])  # admin
                    print (GEGpon[6])  # Subscr
                    print (GEGpon[7])  # Descr ( USED )"""


                    csvLine.append(GEData[1])
                    csvLine.append(GEData[5])
                    csvLine.append(GEData[6])
                    csvLine.append(GEData[7])
                    csvLine.append(GEData[8])
                    csvLine.append(GEData[9])
                    csvLine.append(GEGpon[7])




                    newCSVLines.append(csvLine)

        print (newCSVLines)
        for x in newCSVLines:
            print (x)



    def listToString(self, list):
        for lists in list:
            stringy = ",".join(lists)



    def externalProcess(self, commandString):
        subprocess.call(commandString, shell=True)



GponCombiner()


