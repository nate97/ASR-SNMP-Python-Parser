import os
import time

### GLOBALS ###

# COMMANDS #
SNMP_COMMAND = 'snmpwalk -Os -c %s -v %s %s %s' # community, version, URL, OID

# OID TYPES #
TYPE_INDEX = 'ifIndex'
TYPE_DESCR = 'ifDescr'
TYPE_STATSIN = 'ipIfStatsInOctets'
TYPE_STATSOUT = 'ipIfStatsOutOctets'

# VALID PORTCHANNEL TYPES #
PORTCHANNEL10 = 'Port-channel10'
PORTCHANNEL11 = 'Port-channel11'


class OIDParser():

    def __init__(self):
        pass
        

    # KEEP OID LISTS IN HERE, [NOT] GLOBAL
    def OIDManager(self):
        # We will process and keep track of all OID data HERE

        # Dictionary that contains customer data with VLAN and data usage
        self.customerDict = {} # This will inevitably be the dictionary where we export the data to either a YAML file or YAML files, for individual customers

        # Stores descr data from ASR, includes VLANs
        self.descrDict = {}

        # Key is SNMP index value
        self.octetInDict = {}
        self.octetOutDict = {}

        # Combined octets dict, Get index from octetIn and octetOut dicts and combine them into THIS dictionary
        self.octetDict = {}

        ### Get OID strings ###
        descrOIDS = self.getOIDs(TYPE_DESCR)
        statsINOIDS = self.getOIDs(TYPE_STATSIN) # Disable temp
        statsOUTOIDS = self.getOIDs(TYPE_STATSOUT)

        ### Convert OID strings into OID LISTS ###
        self.parseOIDs(descrOIDS, TYPE_DESCR)
        self.parseOIDs(statsINOIDS, TYPE_STATSIN)
        self.parseOIDs(statsOUTOIDS, TYPE_STATSOUT)

        ### COMBINED OID OCTETS ###
        self.CombINOUTOcts()

        ###### TEMP ######
        print (self.descrDict)
        print (self.octetDict)



    def getOIDs(self, OIDType):    # Retrive a specific type of OID(s) ( Called to retrive list of OIDS from ASR, returns string from ASR )
        # Process our predefined global command and put our variables inside of it
        combinedCommand = SNMP_COMMAND % (self.SNMPCommunity, self.SNMPVersion, self.SNMPUrl, OIDType)

        # RawOIDOutput contains all information retrived from the SNMPwalk bash command
        RawOIDOutput = self.externalProcess(combinedCommand)

        return RawOIDOutput


    def parseOIDs(self, oids, type):    # Parse ALL of the different types of oid lists ( Called AFTER getOIDs, parses string )

        # Remove newlines and special characters, appends each line to a list
        oids_list = oids.split("\\n")

        for single_oid in oids_list: # Iterate through the raw oid list

            if " = " not in single_oid: # If the string ( = ) WITH SPACES, is not in the TEXT line, SKIP
                continue

            self.oidTypeSelector(type, single_oid) # Selects which parser to move onto next


    def oidTypeSelector(self, type, single_oid):
        if type == TYPE_DESCR:
            self.parseDescrOIDS(single_oid)
        elif type == TYPE_STATSIN or type == TYPE_STATSOUT:
            self.parseOctetOIDS(type, single_oid)
        else:
            return # Invalid type! SKIP


    # Parses line of an individual device OID for Description VLAN
    def parseDescrOIDS(self, single_oid):    # Parses description OID type

        # If this fails, skip process
        if PORTCHANNEL10 not in single_oid and PORTCHANNEL11 not in single_oid: # If BOTH of these values are NOT in single_oid, SKIP
            return

        stream_3 = single_oid.split(".")  # Split newline into 3 RAW parts, OID description, port_channel, VLAN

        # If this fails, skip process
        if len(stream_3) <= 2: # If list contains less than 3 items, SKIP
            #print ("Warning: stream_3 did not contain 3 items in this OID, SKIPPING (Ignore this.) " + str(stream_3))
            return

        #### PARSE OUT ALL OF THE NECCESSARY VALUES HERE ####

        # Parse our OID INDEX ID HERE
        rawPortchannelVLAN = stream_3[1] # Extract INDEX and Portchannel
        rawIndexPortchannel = rawPortchannelVLAN.split(" = ") # Portchannel and INDEX spliced apart
        oidIndex = rawIndexPortchannel[0] # OID INDEX, FINISHED WITH THIS


        # Parse out portchannel HERE
        rawPortchannel = rawIndexPortchannel[1] # Extract Portchannel line
        oidPortchanTEMP = rawPortchannel.split(": ") # Splice apart useless junk and Portchannel
        oidPortchannel = oidPortchanTEMP[1] # Portchannel, FINISHED WITH THIS

        # Parse out VLAN tag HERE
        oidVlanTag = stream_3[2]  # Extract VLAN tag [] FINISHED WITH THIS

        #### Append all of our data to our local list HERE ####
        # Append our key ( OID INDEX ), and values ( contained in a list ) to the global descrDict dictionary
        self.descrDict[oidIndex] = (oidPortchannel, oidVlanTag) # Append key and list  to global descrDict


    # Parses line of individual device for OID octets ( Argument should specify wether octet are IN or OUT )
    def parseOctetOIDS(self, type, single_oid):    # Parses IN or OUT octet OID type
        oid = single_oid.split(".")

        # Get rid of OID if it's for IPV6
        if oid[1] == "ipv6":
            return

        oid_index_octet = oid[2].split(" = ")
        oid_index = oid_index_octet[0]

        octet_data = oid_index_octet[1]
        octet_split_bwith = octet_data.split(": ")
        octet_data = octet_split_bwith[1]

        # Choose which dictionary to append octet to
        if type == TYPE_STATSIN:
            octet = octet_data + ' IN'
            self.octetInDict[oid_index] = (octet)
        elif type == TYPE_STATSOUT:
            octet = octet_data + ' OUT'
            self.octetOutDict[oid_index] = (octet)


    def CombINOUTOcts(self):
        combinedOcts = []



        for oidIndex in self.octetInDict:
            single_oid = []

            single_oid.append(self.octetInDict.get(oidIndex))
            single_oid.append(self.octetOutDict.get(oidIndex))

            self.octetDict[oidIndex] = (single_oid)










    # This is done last as a seperate process combining the octets and descr
    # Return if index values the same
    def compareOIDIndex(self, oid_ind_00, oid_ind_01):
        pass