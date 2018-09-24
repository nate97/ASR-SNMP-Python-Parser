import time
import csv

### GLOBALS ###

# PHRASES TO APPEND TO DATA ( For readability ) #
HEADERLIST = ["Index", "Portchannel", "Vlan", "In octet",
              "Out octet", "Timestamp", "Region",
              "Speed Package", "Description",
              "ONT", "IP Address", "Mac address"]  # Needs to be placed in globals

# Folder locations #
MANUALFOLDER = 'CSV_Sources/' # Location of static data CSV files (Must be enerated with provided CSV tools)
STATICDATACSV = 'USERS.csv'

EXPORTFOLDER = 'Customer_Database/' # CSV export folder, this is where we export our completed CSV files to

# Exported file names #
EXPORTFILENAME = '%scustomer-data-%s.csv' # filename that will be used for exported CSV files ( '%s' denotes where the data will be shoved into string, e.g., CUSTOMER_DATA_CSV, 2018-01-01-100000 )



class CSVManager():

    def __init__(self):
        pass


        
    # Read AE csv, export combined data
    def readUsersCsv(self, customerDict):
        self.customerList = []

        with open(MANUALFOLDER + STATICDATACSV) as csvUsersFile:
            readCSV = csv.reader(csvUsersFile, delimiter=',')

            for row in readCSV:
                csvList = [] # List to append all CSV data

                region = (row[0]) # region
                service = (row[1]) # Service type
                outTag = (row[2]) # Out tag
                inTag = (row[3]) # In tag

                if len(inTag) == 3: # Fix inTag by padding it with extra zero when neccessary
                    inTag = '0' + str(inTag)
                    #print ("intag???")

                ID = (row[4]) # ID
                descr = (row[5]) # Description
                ont = (row[6]) # ONT
                ipAddr = (row[7]) # Ip address
                macAddr = (row[8]) # Mac address

                customerVlan = (outTag + inTag)

                for x in customerDict.values():
                    index = x[0][0]
                    portc = x[0][1]
                    asrVlan = str(x[0][2])

                    inOct = x[1][0]
                    outOct = x[1][1]
                    timeStamp = x[1][2]

                    if customerVlan == asrVlan: # If the VLANS match, the data for this line IS related and can be appended
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
        csvUsersFile.close()



    # Exports combined ASR AE CSV files
    def exportCustomerData(self):
        print ("EXPORTING DATA!")
        # Get current time to append to file name.
        time = self.createFileTimestamp()

        openFileStr = EXPORTFILENAME % (EXPORTFOLDER, time) # Merges export folder/name and timestamp into the string used for creating a file in a specified path

        # Create a CSV file to put our merged data from AE and ASR in
        with open(openFileStr, 'w') as csvCustomer:
            writeCSV = csv.writer(csvCustomer)

            # This is just for human readability, adds headers to the CSV file
            writeCSV.writerow(HEADERLIST) # TEMP

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
                descr = customer[8]
                ont = customer[9]
                ipAddr = customer[10]
                macAddr = customer[11]

                tempList.append(index)
                tempList.append(portc)
                tempList.append(vlan)
                tempList.append(inOct)
                tempList.append(outOct)
                tempList.append(timeStamp)
                tempList.append(region)
                tempList.append(speedPackage)
                tempList.append(descr)
                tempList.append(ont)
                tempList.append(ipAddr) # IP Address
                tempList.append(macAddr) # Mac Address

                writeCSV.writerow(tempList)

        # Close our merged ASR, CSV file
        csvCustomer.close()


