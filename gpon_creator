import subprocess
import datetime
import time
import os
import csv
import argparse
import os.path

### GLOBALS ###

#### Variables for header names ####

REGION = " REGION "
NETWORK = " NETWORK "
INTF = " INTF "
ADMIN = " ADMIN "
SUBSCRID = " SUBSCR-ID "
DESCR = " DESCR "
ONT = " ONT "
ID = " ID "
OUTTAG = " OUT-TAG "
INTAG = " IN-TAG "
TAGACTION = " TAG-ACTION "
BWPROF = " BW-PROF "
MCASTPROF = " MCAST-PROF "

# File paths #
FIXEDPATH = "combine_gpon/"

# HEADER #
HEADER = ""

# FILE NAMES #
EXPORTFILENAME = "GPON.csv"
FILE1 = "gpon_ont_ge.csv"
FILE2 = "gpon_data.csv"


class gponCreator():

    def __init__(self):
        print ("CMS GPON file combiner")

        self.userInput()



    def userInput(self):
        print ("Enter name of your csv files, located in directory combine_gpon/")
        self.file1 = input("(DEFAULT: gpon_ont_ge.csv) GE file: ")
        self.file2 = input("(DEFAULT: gpon_data.csv) Data file: ")

        if self.file1 == "" or self.file2 == "":
            self.file1 = FILE1
            self.file2 = FILE2

        self.file1 = FIXEDPATH + self.file1
        self.file2 = FIXEDPATH + self.file2

        if os.path.exists(self.file1) and os.path.exists(self.file2):
            pass
        else:
            print ("File(s) not found.")
            return

        self.file1Fixed = self.file1.split(".")[0] + "_fixed.csv"
        self.file2Fixed = self.file2.split(".")[0] + "_fixed.csv"

        self.mergeManager()



    def mergeManager(self):
        # Figure out which columns the required data is located at
        self.headerKeysGE = self.getColumnPosition(self.file1) # Calculate index values for header names
        self.headerKeysDATA = self.getColumnPosition(self.file2) # Calculate index values for header naems

        # This is to remove the unneccessary lines from our CSV files!
        self.externalProcess("awk 'NR>2' " + self.file1 + " > " + self.file1Fixed) # Remove first two lines of first CSV file, ( GE File )
        self.externalProcess("awk 'NR>2' " + self.file2 + " > " + self.file2Fixed) # Remove first two lines of second CSV file, ( DATA File )

        # Function merges the two provided CSV files
        self.CSVCombiner(self.file1Fixed, self.file2Fixed) # Open both CSV files to be merged

        # Delete no longer neccessary temp files
        self.externalProcess("rm " + self.file1Fixed)
        self.externalProcess("rm " + self.file2Fixed)



    def getColumnPosition(self, filename):
        fileA = open(filename) # Open file
        lines = fileA.readlines() # Read file

        # Hederkey list curating
        headerKeys = lines[1].split(",") # Split the second line of csv file into a list
        del headerKeys[-1] # Deletes last item of list, THIS SHOULD BE THE NEW LINE DELIMITER (\n)
        columnCount = len(headerKeys) # Get the count of items in headerKeys

        # Column name to position
        headerConverter = {} # IMPORTANT # This is where we place our keys and values into, example: position 5 is the ID header.
        for y in range(0, columnCount): # Iterates over amount of items in columnCount
            headerConverter[headerKeys[y]] = y # Appends the header name as the key, and the value as the integer location of header

        return headerConverter # Returns dictionary



    def CSVCombiner(self, file1, file2):
        # First variable is the opened file in python, the second variable is the python CSV pointer ( these are important )
        newReader1, newFile1 = self.openCSV(FIXEDPATH + EXPORTFILENAME, "w") # File to write to, defined in the global variables at the top
        csvFileReader1, csvFile1 = self.openCSV(file1, "r")
        csvFileReader2, csvFile2 = self.openCSV(file2, "r")

        mergedData = [] # Where all of our merged data from each file goes

        # Convert both of our files into a list so we can easily iterate over their data
        file1List = self.file2List(csvFileReader1)
        file2List = self.file2List(csvFileReader2)

        for rowsGE in file1List: ##### GE File ##### FIRST FILE
            regionGE = rowsGE[self.headerKeysGE[REGION]]  # Extract position of region from headerKeysGE
            descrGE = rowsGE[self.headerKeysGE[DESCR]]
            idGE = rowsGE[self.headerKeysGE[ONT]]

            # FILTER #
            ##### IGNORE THE JUNK DATA #####
            if descrGE == " ":
                continue
            if regionGE == " ":
                continue
            if idGE == " ":
                continue

            for rowsDATA in file2List: ##### Data File ##### SECOND FILE
                regionData = rowsDATA[self.headerKeysDATA[REGION]]
                descrData = rowsDATA[self.headerKeysDATA[DESCR]]
                idData = rowsDATA[self.headerKeysDATA[ID]]
                octetOutData = rowsDATA[self.headerKeysDATA[INTAG]]

                # FILTER #
                ##### IGNORE THE JUNK DATA #####
                if regionData == " ":
                    continue
                if idData == " ":
                    continue
                if octetOutData == "Not Used": # THIS MIGHT NOT BE THE CORRECT THING TODO!!!
                    continue

                # Special case that formats our data correctly
                idData = self.IDCorrector(idData) # Correct the format of the data in ID column

                # IF we have a collision, continue
                if regionGE == regionData and idGE == idData: # If we have a match on a single line ( IN BOTH FILES ) we will merge that data
                    #print ("Collision")

                    collidedDataList = [] # This is the list we append our collided data from the two files into, one is generated for EACH customer

                    collidedDataList.append(rowsDATA[self.headerKeysDATA[NETWORK]])
                    collidedDataList.append(rowsDATA[self.headerKeysDATA[BWPROF]])
                    collidedDataList.append(rowsDATA[self.headerKeysDATA[OUTTAG]])
                    collidedDataList.append(rowsDATA[self.headerKeysDATA[INTAG]])
                    collidedDataList.append(rowsDATA[self.headerKeysDATA[MCASTPROF]])
                    collidedDataList.append(rowsDATA[self.headerKeysDATA[ID]])
                    collidedDataList.append(rowsGE[self.headerKeysGE[DESCR]]) # GE
                    collidedDataList.append(rowsGE[self.headerKeysGE[ONT]]) # GE

                    mergedData.append(collidedDataList)

        # Crappy solution to export data to the new CSV file
        for data in mergedData:
            stringy = ",".join(data)
            newFile1.write(stringy + "\n")



    # Opens a provided file and then opens the file with CSV reader
    def openCSV(self, filename, openType):
        fileObject = open(filename, openType)
        csvReaderObject = csv.reader(fileObject, delimiter=',')
        return csvReaderObject, fileObject



    # Iterates over every line in file and places them into a list
    def file2List(self, filename):
        fileList = []  # Place all valid data from csv file in here

        for line in filename:
            fileList.append(line) # Append our line list to a static list

        return fileList



    # Removes extraneous garbage off of ID field FROM the (DATA) file
    def IDCorrector(self, ID):
        correctedID = ID # Default failover

        id = ID.split("-GE") # Remove the -GE
        id = id[0] # Selects the correct string from previous statement

        try:
            id = id.split("-", 1) # Split the second dash
            correctedID = (id[1]) # Select the correct string from previous statement
        except:
             pass

        return correctedID



    # Runs external bash commands
    def externalProcess(self, command):
        subprocess.call(command, shell=True)



gponCreator()


