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
MANUAL_FOLDER = 'MANUAL_CSV/'
GPON_FOLDER = 'GPON_CSV/'


class CSVManager():

    def __init__(self):
        print ('CSV Manager...')



    # Exports a single session walk from the ASR to CSV
    def exportAsrSNMPData(self, customerDict):
        #### !!! CSV EXPORTER !!! ####
        with open('Customer_data.csv', 'w') as f:
            w = csv.writer(f)

            header_dict = [INDEXPHRASE, PORTCHANPHRASE, VLANPHRASE, INPHRASE, OUTPHRASE, TIMEPHRASE]
            w.writerow(header_dict)

            for x in customerDict.values():

                csv_list = []

                index = x[0][0]
                portc = x[0][1]
                vlan = x[0][2]

                inOct = x[1][0]
                outOct = x[1][1]
                timeStamp = x[1][2]

                csv_list.append(index)
                csv_list.append(portc)
                csv_list.append(vlan)

                csv_list.append(inOct)
                csv_list.append(outOct)
                csv_list.append(timeStamp)

                w.writerow(csv_list)
                


    # Read GPON csv, export combined data
    def readGPONcsv(self, customerDict):

        combined_list = []

        with open(MANUAL_FOLDER + 'GPON.csv') as csvGPON:
            readCSV = csv.reader(csvGPON, delimiter=',')

            for row in readCSV:
                csv_list = []

                network = (row[0])

                oTag = (row[2])
                iTag = (row[3])
                gpon_vlan = (str(oTag) + str(iTag))


                ID_1 = (row[5])
                ID_2 = (row[6])
                match_1 = (row[7])
                descr =  (row[12])
                ont = (row[13])

                for x in customerDict.values():

                    index = x[0][0]
                    portc = x[0][1]
                    asr_vlan = str(x[0][2])

                    inOct = x[1][0]
                    outOct = x[1][1]
                    timeStamp = x[1][2]

                    if gpon_vlan == asr_vlan:
                        csv_list.append(index)
                        csv_list.append(portc)
                        csv_list.append(asr_vlan)
                        csv_list.append(inOct)
                        csv_list.append(outOct)
                        csv_list.append(timeStamp)

                        csv_list.append(network)
                        csv_list.append(ID_1)
                        csv_list.append(match_1)
                        csv_list.append(descr)
                        csv_list.append(ont)

                        combined_list.append(csv_list)
        # Close the GPON csv file
        csvGPON.close()


        ###### SHOULD BE A NEW FUNCTION. ######

        # Get current time to append to file name.
        time = self.createFileTimestamp()

        # Create a CSV file to put our merged data from GPON and ASR in
        with open(GPON_FOLDER + 'gpon-customer-data-' + time + '.csv', 'w') as csvGPONcustomer:
            a = csv.writer(csvGPONcustomer)

            # This is just for human readability, adds headers to the CSV file
            header_dict = [INDEXPHRASE, PORTCHANPHRASE, VLANPHRASE, INPHRASE, OUTPHRASE, TIMEPHRASE, "NETWORK", "ID", "MATCH", "DESCRIPTION", "ONT"] # Needs to be placed in globals
            a.writerow(header_dict)

            for customer in combined_list:
                temp_list = []

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

                temp_list.append(index)
                temp_list.append(portc)
                temp_list.append(vlan)
                temp_list.append(inOct)
                temp_list.append(outOct)
                temp_list.append(timeStamp)

                temp_list.append(network)
                temp_list.append(ID)
                temp_list.append(match)
                temp_list.append(descr)
                temp_list.append(ont)

                a.writerow(temp_list)

        # Close our merged ASR, GPON CSV file
        csvGPONcustomer.close()
