import subprocess
import datetime
import time
import os

import yaml

from oid_parser import OIDParser
from gp_manager import GPONManager
from ae_manager import AEManager


### GLOBALS ###

# FILES #
CREDENTIALSFILE = 'credentials.yaml' # File contains all credentials of machines that we may want to access

# Heading keys #
ASRCREDSKEY = 'rtl1-credentials' # Dictionary name that contains info to access device (This is located in credentials.yaml)

# Time delay before we poll ASR #
DELAY = 10 # In seconds


class ASRDataExtractor(OIDParser, GPONManager, AEManager):

    def __init__(self):
        print ("Application ran at: " + self.createFileTimestamp())

        self.getCredentials()
        self.mainManager()


    def mainManager(self):
        while True: # This while statement should be removed when ready to have this script run as a CRON JOB
            self.OIDManager()  # Located in class OIDParser
            self.readGPONcsv(self.customerDict)
            self.exportGPONCustomerData()

            self.OIDManager()  # Located in class OIDParser
            self.readAEcsv(self.customerDict)
            self.exportAECustomerData()

            time.sleep(DELAY)


    def getCredentials(self):
        # Open the credentials.yaml file so we can parse it
        yamlCredsFile = self.openYAML(CREDENTIALSFILE) # CREDENTIALS_FILE is a global variable

        # Get the appropriate credentials out of the YAML data stream
        ASRCreds =  (yamlCredsFile[ASRCREDSKEY]) # DEVICE_YAML_LOGIN is a global variable containing the specific device key for login creds

        ### Retrive SNMP credentials and put them into global class variables ###
        self.SNMPCommunity = ASRCreds["community"]
        self.SNMPVersion = ASRCreds["version"]
        self.SNMPUrl = ASRCreds["URL"]


    # Opens a yaml file and returns data stream
    def openYAML(self, filename):
        with open(filename, 'r') as stream:
            try:
                yamlDataFile = yaml.load(stream)
                return yamlDataFile
            except:
                    print (exc)


    def externalProcess(self, commandString):
        # Run bash command
        bashProcess = subprocess.Popen(commandString.split(), stdout = subprocess.PIPE)
        # Put output from the bash command into a Python variable
        bashOutput, BashError = bashProcess.communicate()
        # Convert the output into a string
        pythonOutput = str(bashOutput)

        return pythonOutput


    # Generates a time stamp in number of seconds from EPOCH time (Jan,1,1970)
    def createTimestamp(self):
        timestamp = time.time()
        return timestamp


    def createFileTimestamp(self):
        # Get current time to append to file name.
        date = datetime.datetime.now()
        filetimestamp = date.strftime("%Y-%m-%d-%H%M%S")
        return filetimestamp


    def octetToMb(self, octet):
        mb = int(octet / 1048576) # Conversion from octet to Mb, converted to integer, strips anything after decimal
        return octet


ASRDataExtractor()


