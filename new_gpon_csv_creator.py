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
                    test = (id2[1])

                    regionAndID = [region + ":" + test] # Create new individual column list
                    row = regionAndID + row # Append new data to our row list
                    gponDataList.append(row)

                except:
                    continue

        csvAE.close()

        return gponDataList



    def repeats(self):

        self.findMatch()

        new1 = self.remove_duplicates(self.gponGeList)

        gponData2 = self.remove_duplicates(self.gponDataList)

        #for x in new1:
            #print (x[0])



    def remove_duplicates(self, listy):
        newlist = [ii for n, ii in enumerate(listy) if ii not in listy[0][:n]]
        return newlist



    def findMatch(self):

        newCSVLines = []

        for d in self.gponGeList:

            for a in self.gponDataList:

                if d[0] in a[0]:

                    print (d)
                    print (d[0])
                    print (d[1])
                    print (d[2])
                    print (d[3])
                    print (d[4])
                    print (d[5])
                    print (d[6])
                    print (d[7])
                    print ("|||||||||||||||||||||||||||||||||")

                    print (a[3])
                    print (a[4])
                    print (a[5])
                    print (a[6])
                    print (a[7])

                    print (a)

                    newCSVLines.append(d[0])
                    newCSVLines.append(d[1])
                    newCSVLines.append(d[2])
                    newCSVLines.append(d[3])
                    newCSVLines.append(d[4])
                    newCSVLines.append(d[5])
                    newCSVLines.append(d[6])
                    newCSVLines.append(d[7])

                    newCSVLines.append(a[3])
                    newCSVLines.append(a[4])
                    newCSVLines.append(a[5])
                    newCSVLines.append(a[6])
                    newCSVLines.append(a[7])

        # WORKS!!!!! DON'T DELETE THIS COMM                    newCSVLines.append(a[])ENT!!!!!!!!!! USED AS REFERENCE!!!!!!!!!!!
        """
        for x in range(0, len(self.gponGeList)):
            try:
                if "Cave In Rock:1-1-94" in self.gponDataList[x]:
                    print ("In lists")
            except:
                pass
                
        """



    def listToString(self, list):
        for lists in list:
            stringy = ",".join(lists)



    def externalProcess(self, commandString):
        subprocess.call(commandString, shell=True)



GponCombiner()