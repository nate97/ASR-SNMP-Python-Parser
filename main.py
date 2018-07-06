import subprocess
import datetime
import time
import os

import yaml

from oid_parser import OIDParser


### GLOBALS ###

# FILES #
CREDENTIALS_FILE = 'credentials.yaml' # File contains all credentials of machines that we may want to access

# Heading keys #
ASR_CREDS_KEY = 'rtl1-credentials' # Dictionary name that contains info to access device (This is located in credentials.yaml)



class ASRDataExtractor(OIDParser):

    def __init__(self):

        # Load OID parser
        OIDParser.__init__(self)

        self.getCredentials()

        self.OIDManager() # Located in class OIDParser



    def getCredentials(self):
        # Open the credentials.yaml file so we can parse it
        yamlCredsFile = self.openYAML(CREDENTIALS_FILE) # CREDENTIALS_FILE is a global variable

        # Get the appropriate credentials out of the YAML data stream
        ASRCreds =  (yamlCredsFile[ASR_CREDS_KEY]) # DEVICE_YAML_LOGIN is a global variable containing the specific device key for login creds

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



ASRDataExtractor()


