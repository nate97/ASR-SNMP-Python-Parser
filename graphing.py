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



    def graphPrerequisites(self, customerList):
        timeSeconds = []
        outUsage = []
        timeList = []
        firstSample = True

        #print (customerList)

        for uu in customerList[10]:
            outOctet = (int(uu[1]))
            outOctet = self.octetToMb(outOctet)
            time = (float(uu[2]))

            outUsage.append(outOctet)

            if not firstSample:
                # Visual data, this is what we draw on the png file for the time scale
                timeStr = datetime.datetime.fromtimestamp(time).strftime('%m/%d %H:%M')
                timeList.append(timeStr)

            # Seconds
            timeSeconds.append(time)
            firstSample = False

        outUsageDiff = [outUsage[i + 1] - outUsage[i] for i in range(len(outUsage) - 1)]
        timeDiff = [timeSeconds[i + 1] - timeSeconds[i] for i in range(len(timeSeconds) - 1)]

        sortedUsageDiff = sorted(outUsageDiff)
        length = len(sortedUsageDiff)
        count = len(outUsageDiff)
        calcC = round((length * 0.95))
        bpsList = self.calculateBPS(count, outUsageDiff, timeDiff)  # Calls function

        self.createGraph(timeList, bpsList)



    # Allows us to view the maximum data downloaded and uploaded by the customer based off the octets
    def getMaxUsage(self):
        pass


    def createGraph(self, timeList, bpsList):
        fig, ax = plt.subplots(nrows=1, ncols=1)  # create figure & 1 axis
        fig.set_size_inches(20, 10.0, forward=True)

        fig.subplots_adjust(bottom=.25)


        plt.xlabel(xLABEL)
        plt.ylabel(yLABEL)

        #plt.xlim([0, 10])
        plt.ylim(0.0, 5.0)

        #ax.plot(timeList, bpsList, marker='o', markevery=9)
        ax.plot(timeList, bpsList)

        locs, labels = plt.xticks()
        #labelList = self.removeEveryOther(locs)
        labelList = self.removeExtraneous(locs)

        plt.xticks(rotation=50)
        plt.xticks(labelList)

        #plt.show()
        fig.savefig(GRAPH_FILENAME,bbox_inches='tight')  # save the figure to file
        plt.close(fig)  # close the figure



    def calculateBPS(self, count, usageDiff, timeDiff):
        bpsList = [] # Put our bits per second in list

        for x in range(0, count):
            dataSample = usageDiff[x]
            timePeriod = timeDiff[x]
            bitsPerSec = (dataSample / timePeriod)

            bpsList.append(bitsPerSec)

        return bpsList



    # Removes extraneous labels from our X axis
    def removeExtraneous(self, theList):
        length = len(theList)

        cut = int((length / 3) * (length / (5 * length)))

        if cut == 0:
            return theList

        return theList[::cut]



graphingManager()


