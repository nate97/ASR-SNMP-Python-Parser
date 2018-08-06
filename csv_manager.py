import time
import csv

### GLOBALS ###

# PHRASES TO APPEND TO DATA ( For readability ) #
HEADERLIST = ["Index", "Portchannel", "Vlan", "In octet",
              "Out octet", "Timestamp", "Network",
              "ID", "Match", "Description",
              "ONT", "LinkedPort", "IP address"]  # Needs to be placed in globals

# Folder locations #
MANUALFOLDER = 'MANUAL_CSV/'
GPONFOLDER = 'GPON_CSV/'



class CSVManager():

    def __init__(self):
        print ('GPON CSV Manager...')



    # Read GPON csv, export combined data
    def readGPONcsv(self, customerDict):

        self.customerList = []

        with open(MANUALFOLDER + 'GPON.csv') as csvGPON:
            readCSV = csv.reader(csvGPON, delimiter=',')

            for row in readCSV:
                csvList = []

                network = (row[0])

                oTag = (row[2])
                iTag = (row[3])
                gponVlan = (str(oTag) + str(iTag))

                ID1 = (row[5])
                ID2 = (row[6])
                match1 = (row[7])
                descr =  (row[12])
                ont = (row[13])

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

                        csvList.append(network)
                        csvList.append(ID1)
                        csvList.append(match1)
                        csvList.append(descr)
                        csvList.append(ont)

                        self.customerList.append(csvList)
        # Close the GPON csv file
        csvGPON.close()



    # Exports combined ASR GPON CSV files
    def exportGPONCustomerData(self):
        print ("Exporing GPON csv data...")
        # Get current time to append to file name.
        time = self.createFileTimestamp()

        # Create a CSV file to put our merged data from GPON and ASR in
        with open(GPONFOLDER + 'gpon-customer-data-' + time + '.csv', 'w') as csvGPONcustomer:
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

                network = customer[6]
                ID = customer[7]
                match = customer[8]
                descr = customer[9]
                ont = customer[10]

                tempList.append(index)
                tempList.append(portc)
                tempList.append(vlan)
                tempList.append(inOct)
                tempList.append(outOct)
                tempList.append(timeStamp)

                tempList.append(network)
                tempList.append(ID)
                tempList.append(match)
                tempList.append(descr)
                tempList.append(ont)
                tempList.append(' ') # linkedPort
                tempList.append(' ') # IP address

                writeCSV.writerow(tempList)

        # Close our merged ASR, GPON CSV file
        csvGPONcustomer.close()
