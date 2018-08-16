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



    def first(self):
        self.externalProcess("awk 'NR>2' combine_gpon/gpon_ont_ge.csv > combine_gpon/gpon_ont_ge_nohead.csv")
        self.externalProcess('sort ' + 'combine_gpon/gpon_ont_ge_nohead.csv' +  ' > ' + 'combine_gpon/gpon_ont_ge_sorted.csv') # Sort
        gponGeList = self.iterateGeCSV('combine_gpon/gpon_ont_ge_sorted.csv')

        self.duplicates(gponGeList)



    def second(self):
        self.externalProcess("awk 'NR>2' combine_gpon/gpon_data.csv > combine_gpon/gpon_data_nohead.csv")
        self.externalProcess('sort ' + 'combine_gpon/gpon_data_nohead.csv' +  ' > ' + 'combine_gpon/gpon_data_sorted.csv') # Sort
        gponDataList = self.iterateDataCSV('combine_gpon/gpon_data_sorted.csv')



    def lineIterator(self, filename):
        lineList = []
        fileA = open(filename, 'r')

        for line in fileA.readlines():
            print (line)
            lineList.append(line)

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

                regionAndID = [region + ":" + id] # Create new individual column list
                row = regionAndID + row # Append new data to our row list
                gponDataList.append(row)

        csvAE.close()

        return gponDataList



    def duplicates(self, lists):

        possibleDupes = []
        realDuplicates = []

        for data in lists:
            possibleDupes.append(data[0])


        noDupes = list(OrderedDict.fromkeys(possibleDupes).keys())

        for x in lists:
            if x[0] in lists:
                print (x[0])



    def listToString(self, list):
        for lists in list:
            stringy = ",".join(lists)



    def externalProcess(self, commandString):
        subprocess.call(commandString, shell=True)



GponCombiner()