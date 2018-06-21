import subprocess
import time
import os

import yaml


### GLOBALS ###

# FILES #
CREDENTIALS_FILE = 'credentials.yaml' # File contains all credentials of machines that we may want to access

# Heading keys #
ASR_CREDS_KEY = 'rtl1-credentials' # Dictionary name that contains info to access device (This is located in credentials.yaml)

# OTHER #
SNMP_COMMAND = 'snmpwalk -Os -c %s -v %s %s %s' # community, version, URL, OID



class ASRParser():

    def __init__(self):
        # Define our class global credentials
        self.getCredentials()
        self.getOID('ifIndex')



    def OIDManager(self):
        # We will process and keep track of all OID data HERE

        # EXAMPLE #
        self.getOID('ifIndex')



    # Retrive a specific type of OID(s)
    def getOID(self, OIDType):
        # Process our predefined global command and put our variables inside of it
        combinedCommand = SNMP_COMMAND % (self.SNMPCommunity, self.SNMPVersion, self.SNMPUrl, OIDType)

        # RawOIDOutput contains all information retrived from the SNMPwalk bash command
        RawOIDOutput = self.externalProcess(combinedCommand)

        print (RawOIDOutput)

        def parseOIDS(self, OIDS):
            pass



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



ASRParser()


