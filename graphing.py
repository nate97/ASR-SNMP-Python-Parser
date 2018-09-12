import datetime
import os

import matplotlib.pyplot as plt
import numpy as np
import datetime

# GLOBALS #
GRAPH_FILENAME = "graph_00.png"
xLABEL = "Date/Time"
yLABEL = "Bandwidth in MBps"



class graphingManager():

    def __init__(self):
        print ("Graphing")



    def graphManager(self, vGraphList): # Visual graph list
        with plt.style.context('ggplot'): # This is the style of the graph
            #self.graph(customerList)
            self.createCustomerGraph(vGraphList[0], vGraphList[1], vGraphList[2], vGraphList[3], vGraphList[4], vGraphList[5], vGraphList[6])



    def createCustomerGraph(self, timeList, bpsList, service, customerName, region, vlan, package):
        serviceDwnSpd = service[1] # Download speed

        fig, ax = plt.subplots(nrows=1, ncols=1)  # create figure & 1 axis
        fig.set_size_inches(20, 10.0, forward=True)

        plt.title(customerName + ', ' + region + ', vlan: ' + vlan + ', Package: ' + package)

        plt.xlabel(xLABEL)
        plt.ylabel(yLABEL)

        plt.ylim(0.0, serviceDwnSpd) # Set minimum and maximum numbers displayed on chart

        #ax.plot(timeList, bpsList, marker='o', markevery=5)
        ax.plot(timeList, bpsList)

        locs, labels = plt.xticks()
        # labelList = self.removeEveryOther(locs)
        labelList = self.removeExtraneous(locs)

        plt.xticks(rotation=50)
        plt.xticks(labelList)

        fig.savefig(GRAPH_FILENAME)  # save the figure to file

        plt.close(fig)  # close the figure



    # Removes extraneous labels from our X axis ( This is just for visual display on the graph )
    def removeExtraneous(self, theList):
        length = len(theList)

        cut = int((length / 3) * (length / (5 * length)))

        if cut == 0:
            return theList

        return theList[::cut]



graphingManager()


