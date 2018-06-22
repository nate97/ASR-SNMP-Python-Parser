import os
import time

### GLOBALS ###

# COMMANDS #
SNMP_COMMAND = 'snmpwalk -Os -c %s -v %s %s %s' # community, version, URL, OID

# OID TYPES #
OID_INDEX = 'ifIndex'
OID_DESCR = 'ifDescr'
OID_STATSIN = 'ipIfStatsInOctets'
OID_STATSOUT = 'ipIfStatsOutOctets'



class OIDParser():

    def __init__(self):
        print ('test')
        


    def OIDManager(self):
        # We will process and keep track of all OID data HERE

        # EXAMPLE #
        descrOIDS = self.getOIDs(OID_DESCR)
        statsINOIDS = self.getOIDs(OID_STATSIN)
        statsOUTOIDS = self.getOIDs(OID_STATSOUT)



    def getOIDs(self, OIDType):    # Retrive a specific type of OID(s) ( Called to retrive list of OIDS from ASR, returns string from ASR )
        # Process our predefined global command and put our variables inside of it
        combinedCommand = SNMP_COMMAND % (self.SNMPCommunity, self.SNMPVersion, self.SNMPUrl, OIDType)

        # RawOIDOutput contains all information retrived from the SNMPwalk bash command
        RawOIDOutput = self.externalProcess(combinedCommand)

        print (RawOIDOutput)

        return RawOIDOutput
        


    def parseOIDs(self, OIDS):    # Parse ALL of the different types of oid lists ( Called AFTER getOIDs, parses string )
        pass



    def parseDescrOIDS(self):
        pass
        return OIDLIST



    def parseOctetOIDS(self, type):
        pass
        return OIDLIST