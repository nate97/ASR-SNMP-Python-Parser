import time
import csv

### GLOBALS ###

# PHRASES TO APPEND TO DATA ( For readability ) #
HEADERLIST = ["Index", "Portchannel", "Vlan", "In octet",
              "Out octet", "Timestamp", "Region",
              "Speed Package","ID", "Description",
              "ONT", "IP Address", "Mac address"]  # Needs to be placed in globals

# Folder locations #
MANUALFOLDER = 'CSV_Sources/' # Location of static data CSV files (Must be enerated with provided CSV tools)
STATICDATACSV = 'GPON.CSV'

EXPORTFOLDER = 'Customer_Database/' # CSV export folder, this is where we export our completed CSV files to

# Exported file names #
GPONFILENAME = '%sgp-customer-data-%s.csv' # filename that will be used for exported CSV files ( '%s' denotes where the data will be shoved into string, e.g., CUSTOMER_DATA_CSV, 2018-01-01-100000 )



class GPONManager():

    def __init__(self):
        pass

        

    # Read GPON csv, export combined data
    def readGPONcsv(self, customerDict):

        self.customerList = []

        with open(MANUALFOLDER + STATICDATACSV) as csvGPON:
            readCSV = csv.reader(csvGPON, delimiter=',')

            for row in readCSV:
                csvList = []

                region = (row[0])
                speedPackage = (row[1])

                oTag = (row[2])
                iTag = (row[3])
                gponVlan = (str(oTag) + str(iTag)) # This merges our tags into single VLAN

                ID = (row[4])
                descr =  (row[5])
                ont = (row[6])

                for x in customerDict.values():

                    index = x[0][0]
                    portc = x[0][1]
                    asrVlan = str(x[0][2])

                    inOct = x[1][0]
                    outOct = x[1][1]
                    timeStamp = x[1][2]

                    if gponVlan == asrVlan: # If the VLANS match, the data for this line is related and can be appended
                        csvList.append(index)
                        csvList.append(portc)
                        csvList.append(asrVlan)
                        csvList.append(inOct)
                        csvList.append(outOct)
                        csvList.append(timeStamp)

                        csvList.append(region)
                        csvList.append(speedPackage)
                        csvList.append(ID)
                        csvList.append(descr)
                        csvList.append(ont)

                        self.customerList.append(csvList)
        # Close the GPON csv file
        csvGPON.close()


    # Exports combined ASR GPON CSV files
    def exportGPONCustomerData(self):
        print ("EXPORTING GPON DATA!")
        # Get current time to append to file name.
        time = self.createFileTimestamp() # Get current time to append to file name.

        openFileStr = GPONFILENAME % (EXPORTFOLDER, time) # Merges export folder/name and timestamp into the string used for creating a file in a specified path

        # Create a CSV file to put our merged data from GPON and ASR in
        with open(openFileStr, 'w') as csvGPONcustomer:
            writeCSV = csv.writer(csvGPONcustomer)

            # This is just for human readability, adds headers to the CSV file
            writeCSV.writerow(HEADERLIST)

            for customer in self.customerList:
                tempList = []

                index = customer[0]
                portc = customer[1]
                vlan = customer[2]
                inOct = customer[3]
                outOct = customer[4]
                timeStamp = customer[5]

                region = customer[6]
                speedPackage = customer[7]
                ID = customer[8]
                descr = customer[9]
                ont = customer[10]

                tempList.append(index)
                tempList.append(portc)
                tempList.append(vlan)
                tempList.append(inOct)
                tempList.append(outOct)
                tempList.append(timeStamp)

                tempList.append(region)
                tempList.append(speedPackage)
                tempList.append(ID)
                tempList.append(descr)
                tempList.append(ont)
                tempList.append(' ') # IP Address
                tempList.append(' ') # Mac Address

                writeCSV.writerow(tempList)

        # Close our merged ASR, GPON CSV file
        csvGPONcustomer.close()

