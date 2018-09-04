import time
import csv


### GLOBALS ###

# This is for calculating the cTag based off of the customers region for Active E #
REGIONDICT = {  ########## ADD NEW REGIONS IN THIS DICTIONARY!!! ###########
    "Leamington": "705",
    "Cave In Rock": "805",
    "Elizabethtown": "905",
    "Rosiclare": "1005",
    "Golconda": "1105",
    "Renshaw": "1205",
    "Simpson": "1305",
    "Eddyville": "1405",
    "Hicks": "1505",
    "Equality": "1605",
    "Anna": "1705",
    "Vienna": "1805" }

# PHRASES TO APPEND TO DATA ( For readability ) #
HEADERLIST = ["Index", "Portchannel", "Vlan", "In octet",
              "Out octet", "Timestamp", "Network",
              "ID", "Match", "Description",
              "ONT", "LinkedPort", "IP address"] # This list is for human readability. If someone manually opens an exported CSV file it will have headers.

# Folder locations #
MANUALFOLDER = 'MANUAL_CSV/' # Where we place the curated CSV files at
EXPORTFOLDER = 'CUSTOMER_DATA_CSV/' # CSV export folder, this is where we export our completed CSV files to



class AEManager():


    def __init__(self):
        pass


    # Read AE csv, export combined data
    def readAEcsv(self, customerDict):

        self.customerList = []

        with open(MANUALFOLDER + 'AE.csv') as csvAE:
            readCSV = csv.reader(csvAE, delimiter=',')

            for row in readCSV:
                # FILTER #
                # Bypasses any errors or useless data in CSV file #
                if row[3] == ' ': # If column 3 has no description skip it
                    continue

                csvList = [] # List to append all CSV data

                region = (row[0]) # region
                service = (row[1]) # Service type
                outTag = (row[2]) # Out tag
                inTag = (row[3]) # In tag
                ID = (row[4]) # ID
                descr = (row[5]) # Description
                ont = (row[6]) # ONT
                ipAddr = (row[7]) # Ip address
                macAddr = (row[8]) # Mac address

                aeVlan = (outTag + inTag)


                # UNUSED!!!
                """#cTag = self.calculateCTag(row[9]) # row 9 is linked-port
                #sTag = self.calculateSTag(row[27]) # Row 27 is the region
                #if sTag == None: # This skips appending the customer to our list. Something is wrong with the data.
                #    continue

                #aeVlan = (sTag + cTag)"""

                for x in customerDict.values():
                    index = x[0][0]
                    portc = x[0][1]
                    asrVlan = str(x[0][2])

                    inOct = x[1][0]
                    outOct = x[1][1]
                    timeStamp = x[1][2]

                    if aeVlan == asrVlan: # If the VLANS match, the data for this line IS related and can be appended
                        # Append CSV data to list #
                        csvList.append(index)
                        csvList.append(portc)
                        csvList.append(asrVlan)
                        csvList.append(inOct)
                        csvList.append(outOct)
                        csvList.append(timeStamp)

                        csvList.append(region)
                        csvList.append(service)

                        csvList.append(descr)
                        csvList.append(ont) # ONT

                        csvList.append(ipAddr)
                        csvList.append(macAddr)

                        self.customerList.append(csvList)
        # Close the AE csv file
        csvAE.close()


    # UNUSED!!!
    """# Calculates our Ctag with formula from the linkedPort data for customer, used for vlan
    def calculateCTag(self, linkedPort):
        lPort = linkedPort.split("-")

        cTag = str(int(lPort[0]) * 100 + (int(lPort[1])-1)*24 + int(lPort[2])) # Formula for caluclating cTag

        if len(cTag) <= 3: # Appends a "0" if the cTag is too short ( Is this correct??? )
            cTag = "0" + cTag

        return cTag


    # Calculates Stag based off of region customer is located in, used for vlan
    def calculateSTag(self, region):
        if region in REGIONDICT: # Region is valid and in our GLOBAL region dictionary
            regionCode = REGIONDICT[region]
            #print (regionCode)
        else: # Region was not in dictionary, throw an error to user
            #print ("Invalid region, add region into regionDict if valid. Region is: '" + region + "' otherwise, ignore.")
            regionCode = None

        return regionCode"""



    # Exports combined ASR AE CSV files
    def exportAECustomerData(self):
        print ("EXPORTING ACTIVE-E DATA!")
        # Get current time to append to file name.
        time = self.createFileTimestamp()

        # Create a CSV file to put our merged data from AE and ASR in
        with open(EXPORTFOLDER + 'ae-customer-data-' + time + '.csv', 'w') as csvAEcustomer:
            writeCSV = csv.writer(csvAEcustomer)

            # This is just for human readability, adds headers to the CSV file
            #writeCSV.writerow(HEADERLIST) TEMP

            for customer in self.customerList:
                tempList = []

                # This is stupid, should just do this all in one go and comment what pieces are what.
                index = customer[0]
                portc = customer[1]
                vlan = customer[2]
                inOct = customer[3]
                outOct = customer[4]
                timeStamp = customer[5]

                region = customer[6]
                service = customer[7]

                descr = customer[8]

                ID = customer[9]

                ipAddr = customer[10]
                macAddr = customer[11]

                tempList.append(index)
                tempList.append(portc)
                tempList.append(vlan)
                tempList.append(inOct)
                tempList.append(outOct)
                tempList.append(timeStamp)

                tempList.append(region)
                tempList.append(service)
                tempList.append(ID)

                tempList.append(descr)
                tempList.append(" ") # ONT ( not used on AE )
                tempList.append(ipAddr)
                tempList.append(macAddr)

                writeCSV.writerow(tempList)

        # Close our merged ASR, GPON CSV file
        csvAEcustomer.close()

