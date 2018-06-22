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
        pass
        

    # KEEP OID LISTS IN HERE, [NOT] GLOBAL
    def OIDManager(self):
        # We will process and keep track of all OID data HERE

        # EXAMPLE #
        descrOIDS = self.getOIDs(OID_DESCR)
        statsINOIDS = self.getOIDs(OID_STATSIN) # Disable temp
        #statsOUTOIDS = self.getOIDs(OID_STATSOUT)

        self.parseOIDs(descrOIDS)
        self.parseOIDs(statsINOIDS)


    def getOIDs(self, OIDType):    # Retrive a specific type of OID(s) ( Called to retrive list of OIDS from ASR, returns string from ASR )
        # Process our predefined global command and put our variables inside of it
        combinedCommand = SNMP_COMMAND % (self.SNMPCommunity, self.SNMPVersion, self.SNMPUrl, OIDType)

        # RawOIDOutput contains all information retrived from the SNMPwalk bash command
        RawOIDOutput = self.externalProcess(combinedCommand)

        return RawOIDOutput


    def parseOIDs(self, oids):    # Parse ALL of the different types of oid lists ( Called AFTER getOIDs, parses string )

        # Remove newlines and special characters, appends each line to a list
        oids_list = oids.split("\\n")

        for newline in oids_list:    # Iterate through the raw oid list

            if " = " not in newline:    # If the string ( = ) WITH SPACES, is not in newline, SKIP
                continue

            stream_3 = newline.split(".")  # Split newline into 3 parts, OID description, port_channel, VLAN

            try:
                vlanTag = stream_3[2]  # Extract VLAN tag []
                print(vlanTag)
            except:
                print ("Error: " + str(stream_3))


    def parseDescrOIDS(self):    # Parses description OID type
        pass
        return OIDLIST


    # Argument should specify wether octet is IN or OUT
    def parseOctetOIDS(self, type):    # Parses IN or OUT octet OID type
        pass
        # We will put a time stamp with the octets
        return OIDLIST