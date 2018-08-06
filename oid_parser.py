import os
import time
import csv

### GLOBALS ###

# COMMANDS #
SNMPCOMMAND = 'snmpwalk -Os -c %s -v %s %s %s' # community, version, URL, OID

# OID TYPES #
TYPEINDEX = 'ifIndex'
TYPEDESCR = 'ifDescr'
TYPESTATSIN = 'ipIfStatsInOctets'
TYPESTATSOUT = 'ipIfStatsOutOctets'

# VALID PORTCHANNEL TYPES #
PORTCHANNEL10 = 'Port-channel10'
PORTCHANNEL11 = 'Port-channel11'

# PHRASES TO APPEND TO DATA ( For readability ) # # MOVE THIS TO CSV MANAGER #
INDEXPHRASE = ' INDEX'
PORTCHANPHRASE = ' PORTC'
VLANPHRASE = ' VLAN'
INPHRASE = ' IN'
OUTPHRASE = ' OUT'
TIMEPHRASE = ' TIMESTAMP'

class OIDParser():

    def __init__(self):
        pass


    # KEEP OID LISTS IN HERE, [NOT] GLOBAL. This method is called in a for loop in main.py
    def OIDManager(self):
        # We will process and keep track of all OID data HERE

        # Dictionary that contains customer data with VLAN and data usage ( FROM THE ASR )
        self.customerDict = {}  # This will be the dictionary that we export the data to a YAML file

        # Stores descr data from ASR, includes VLANs
        self.descrDict = {}

        # Key is SNMP index value
        self.octetInDict = {}
        self.octetOutDict = {}
        # Combined octets dict, Get index from octetIn and octetOut dicts and combine them into THIS dictionary
        self.octetDict = {}

        # Polls the ASR once
        self.pollASR()



    # Polls ASR once, gets latest port-channel, octet IN OUT data, VLAN tag, and timestamps from all OIDS
    def pollASR(self):
        print ("POLLING ASR")
        ### Get OID strings ###
        descrOIDS = self.getOIDs(TYPEDESCR)
        statsINOIDS = self.getOIDs(TYPESTATSIN) # Disable temp
        statsOUTOIDS = self.getOIDs(TYPESTATSOUT)

        ### Convert OID strings into OID LISTS ###
        self.parseOIDs(descrOIDS, TYPEDESCR)
        self.parseOIDs(statsINOIDS, TYPESTATSIN)
        self.parseOIDs(statsOUTOIDS, TYPESTATSOUT)

        ### COMBINED OID OCTETS ###
        self.CombINOUTOcts()

        ###### TEMP ######
        #print (self.descrDict)
        #print (self.octetDict)

        # Combine all of our SNMP data from ONE polling session
        self.combOctetsDescr() # Each time we poll the ASR for SNMP data will be called a " session ", we will take the data from each session and append it to global customerDict



    def getOIDs(self, OIDType): # Retrive a specific type of OID(s) ( Called to retrive list of OIDS from ASR, returns string from ASR )
        # Process our predefined global command and put our variables inside of it
        combinedCommand = SNMPCOMMAND % (self.SNMPCommunity, self.SNMPVersion, self.SNMPUrl, OIDType)

        # RawOIDOutput contains all information retrived from the SNMPwalk bash command
        RawOIDOutput = self.externalProcess(combinedCommand)

        return RawOIDOutput


    def parseOIDs(self, oids, type):    # Parse ALL of the different types of oid lists ( Called AFTER getOIDs, parses string )

        # Remove newlines and special characters, appends each line to a list
        oidsList = oids.split("\\n")

        for singleOid in oidsList: # Iterate through the raw oid list ONE OID at a time

            if " = " not in singleOid: # If the string ( = ) WITH SPACES, is not in the TEXT line, SKIP
                continue

            self.oidTypeSelector(type, singleOid) # Selects which parser to move onto next


    def oidTypeSelector(self, type, singleOid):
        if type == TYPEDESCR:
            self.parseDescrOIDS(singleOid)
        elif type == TYPESTATSIN or type == TYPESTATSOUT:
            self.parseOctetOIDS(type, singleOid)
        else:
            return # Invalid type! SKIP


    # Parses line of an individual device OID for Description VLAN
    def parseDescrOIDS(self, singleOid):    # Parses description OID type

        # If this fails, skip process
        if PORTCHANNEL10 not in singleOid and PORTCHANNEL11 not in singleOid: # If BOTH of these values are NOT in single_oid, SKIP
            return

        stream3 = singleOid.split(".")  # Split newline into 3 RAW parts, OID description, port_channel, VLAN

        # If this fails, skip process
        if len(stream3) <= 2: # If list contains less than 3 items, SKIP
            #print ("Warning: stream3 did not contain 3 items in this OID, SKIPPING (Ignore this.) " + str(stream3))
            return

        #### PARSE OUT ALL OF THE NECCESSARY VALUES HERE ####

        # Parse our OID INDEX ID HERE
        rawPortchannelVLAN = stream3[1] # Extract INDEX and Portchannel
        rawIndexPortchannel = rawPortchannelVLAN.split(" = ") # Portchannel and INDEX spliced apart
        oidIndex = rawIndexPortchannel[0] # OID INDEX, FINISHED WITH THIS

        # Parse out portchannel HERE #
        rawPortchannel = rawIndexPortchannel[1] # Extract Portchannel line
        oidPortchanTEMP = rawPortchannel.split(": ") # Splice apart useless junk and Portchannel
        oidPortchannel = oidPortchanTEMP[1] # Portchannel, FINISHED WITH THIS

        # Parse out VLAN tag HERE #
        oidVlanTag = stream3[2]  # Extract VLAN tag [] FINISHED WITH THIS

        ### Combine the data we want into a list ###
        descrList = []

        descrList.append(oidIndex) # THIS IS JUST FOR US TO BE ABLE TO SEE THE INDEX WHEN EXTRACTED FROM DICTIONARY, NOT VERY IMPORTANT
        descrList.append(oidPortchannel)
        descrList.append(oidVlanTag)

        #### Append all of our data to our local list HERE ####
        # Append our key ( OID INDEX ), and values ( contained in a list ) to the global descrDict dictionary
        self.descrDict[oidIndex] = (descrList) # Append key and list  to global descrDict


    # Parses line of individual device for OID octets ( Argument should specify wether octet are IN or OUT )
    def parseOctetOIDS(self, type, singleOid):    # Parses IN or OUT octet OID type
        oid = singleOid.split(".")

        # Get rid of OID if it's for IPV6
        if oid[1] == "ipv6":
            return

        oidIndexOctet = oid[2].split(" = ")
        oidIndex = oidIndexOctet[0]

        octetData = oidIndexOctet[1]
        octetSplitBawidth = octetData.split(": ")
        octetData = octetSplitBawidth[1]

        # Choose which dictionary to append octet to
        if type == TYPESTATSIN:
            octet = octetData # ACTUAL DATA
            self.octetInDict[oidIndex] = (octet)
        elif type == TYPESTATSOUT:
            octet = octetData # ACTUAL DATA
            self.octetOutDict[oidIndex] = (octet)


    def CombINOUTOcts(self):
        combinedOcts = []

        for oidIndex in self.octetInDict:
            singleOid = []

            singleOid.append(self.octetInDict.get(oidIndex))
            singleOid.append(self.octetOutDict.get(oidIndex))

            # Special case, append time stamp, doesn't need to be precise, but it is useful to have this
            singleOid.append(str(self.createTimestamp())) # Time stamp is seconds from EPOCH

            self.octetDict[oidIndex] = (singleOid)



    def combOctetsDescr(self):
        print ("MERGING DATA & OIDS")
        for octetIndex in self.octetDict:
            for descrIndex in self.descrDict:

                if octetIndex == descrIndex:

                    self.customerDict[octetIndex] = (self.descrDict.get(octetIndex), self.octetDict.get(octetIndex))

        #print (self.customerDict)


