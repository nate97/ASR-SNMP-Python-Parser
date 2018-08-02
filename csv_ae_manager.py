import time
import csv

### GLOBALS ###

# PHRASES TO APPEND TO DATA ( For readability ) #
INDEXPHRASE = ' INDEX'
PORTCHANPHRASE = ' PORTCHANNEL'
VLANPHRASE = ' VLAN'
INPHRASE = ' IN OCTET'
OUTPHRASE = ' OUT OCTET'
TIMEPHRASE = ' TIMESTAMP'

# Folder locations #
MANUALFOLDER = 'MANUAL_CSV/'
AEFOLDER = 'AE_CSV/'


class AECSVManager():


    def __init__(self):
        print ("AE CSV Manager...")



    # Read AE csv, export combined data
    def readAEcsv(self, customerDict):

        self.customerList = []

        with open(MANUALFOLDER + 'AE.csv') as csvAE:
            readCSV = csv.reader(csvAE, delimiter=',')

            for row in readCSV:


                # Bypasses any errors or useless data in CSV file #
                if "AEONTID" in row[0] or "generated" in row[0]: # Skip the first two useless rows
                    continue
                if row[9] == ' ':
                    continue
                if row[27] == ' ' or row[27] == 'autodiscovered':
                    continue
                if 'NTWK' in row[9]:
                    continue


                csvList = [] # List to append all CSV data

                aeID = (row[0]) # AEONTID
                regID = (row[1]) # REG-ID
                subID = (row[2]) # SUBSCRIBER-ID
                descr = (row[3]) # DESCR
                ontProf = (row[4]) # ONTPROF

                linkedNet = (row[8]) # LINKED NETWORK
                linkedPort = (row[9]) # LINKED PORT
                ipAddr = (row[10]) # IP ADDRESS
                macAddr = (row[11]) # Mac address

                region = (row[27]) # REGION

                cTag = self.calculateCTag(row[9]) # row 9 is linked-port
                sTag = self.calculateSTag(row[27]) # Row 27 is the region

                if sTag == None: # This skips appending the customer to our list. Something is wrong with the data.
                    continue

                aeVlan = (sTag + cTag)


                for x in customerDict.values():
                    index = x[0][0]
                    portc = x[0][1]
                    asrVlan = str(x[0][2])

                    inOct = x[1][0]
                    outOct = x[1][1]
                    timeStamp = x[1][2]

                    if aeVlan == asrVlan: # If the VLANS match, the data for this line is related and can be appended

                        # Append CSV data to list #
                        csvList.append(index)
                        csvList.append(portc)
                        csvList.append(asrVlan)
                        csvList.append(inOct)
                        csvList.append(outOct)
                        csvList.append(timeStamp)

                        csvList.append(region)
                        csvList.append('')
                        csvList.append('')
                        csvList.append(descr)
                        csvList.append(linkedPort)

                        self.customerList.append(csvList)
        # Close the AE csv file
        csvAE.close()
        print (self.customerList)



    def calculateCTag(self, linkedPort):
        lPort = linkedPort.split("-")

        cTag = str(int(lPort[0]) * 100 + (int(lPort[1])-1)*24 + int(lPort[2]))

        if len(cTag) <= 3:
            cTag = "0" + cTag

        return cTag



    def calculateSTag(self, region):
        if region == "Equality":
            regionCode = "1605"
        elif region == "Leamington":
            regionCode = "705"
        elif region == "Cave In Rock":
            regionCode = "805"
        elif region == "Elizabethtown":
            regionCode = "905"
        elif region == "Rosiclare":
            regionCode = "1005"
        elif region == "Golconda":
            regionCode = "1105"
        elif region == "Renshaw":
            regionCode = "1205"
        elif region == "Simpson":
            regionCode = "1305"
        elif region == "Anna":
            regionCode = "1705"
        elif region == "Vienna":
            regionCode = "1805"
        elif region == "Eddyville":
            regionCode = "1405"
        elif region == "Hicks":
            regionCode = "1505"
        else:
            regionCode = None
            print ("Unknown region code: '" + region + "', setting region name to None and skipping customer, add if statement for new regions")

        return regionCode




    # Exports combined ASR AE CSV files
    def exportAECustomerData(self):
        # Get current time to append to file name.
        time = self.createFileTimestamp()

        # Create a CSV file to put our merged data from AE and ASR in
        with open(AEFOLDER + 'ae-customer-data-' + time + '.csv', 'w') as csvAEcustomer:
            writeCSV = csv.writer(csvAEcustomer)

            # This is just for human readability, adds headers to the CSV file
            headerList = [INDEXPHRASE, PORTCHANPHRASE, VLANPHRASE, INPHRASE, OUTPHRASE, TIMEPHRASE, "NETWORK", "ID", "MATCH", "DESCRIPTION", "ONT"] # Needs to be placed in globals
            writeCSV.writerow(headerList)

            for customer in self.customerList:
                tempList = []

                index = customer[0]
                portc = customer[1]
                vlan = customer[2]
                inOct = customer[3]
                outOct = customer[4]
                timeStamp = customer[5]

                region = customer[6]
                ID = customer[7]
                match = customer[8]
                descr = customer[9]
                linkedPort = customer[10]

                tempList.append(index)
                tempList.append(portc)
                tempList.append(vlan)
                tempList.append(inOct)
                tempList.append(outOct)
                tempList.append(timeStamp)

                tempList.append(region)
                tempList.append(ID)
                tempList.append(match)
                tempList.append(descr)
                tempList.append(linkedPort)

                writeCSV.writerow(tempList)

        # Close our merged ASR, GPON CSV file
        csvAEcustomer.close()

