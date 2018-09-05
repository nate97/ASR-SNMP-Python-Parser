import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np

import datetime
import os


# GLOBALS #
GRAPH_FILENAME = "graph_00.png"
xLABEL = "Time"
yLABEL = "Bits"


class graphingManager():

    def __init__(self):
        print ("Graphing")



    def graphPrerequisites(self, customerList):
        timeSeconds = []
        outUsage = []
        timeList = []
        firstSample = True

        for uu in customerList[10]:
            outOctet = (int(uu[1]))
            outOctet = self.octetToMb(outOctet)
            time = (float(uu[2]))

            outUsage.append(outOctet)

            if not firstSample:
                # Visual data, this is what we draw on the png file for the time scale
                timeStr = datetime.datetime.fromtimestamp(time).strftime('%H:%M')
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
        bpsList = self.calculateBPS(count, outUsageDiff, timeDiff) # Calls function

        self.createGraph(timeList, bpsList)



    def createGraph(self, timeList, bpsList):
        fig, ax = plt.subplots(nrows=1, ncols=1)  # create figure & 1 axis
        fig.set_size_inches(10, 10.0, forward=True)


        plt.xlabel(xLABEL)
        plt.ylabel(yLABEL)

        #ax.plot(timeL, bpsList, marker='o', markevery=9)
        ax.plot(timeList, bpsList)

        locs, labels = plt.xticks()
        #labelList = self.removeEveryOther(locs)

        plt.xticks(locs)
        plt.show()
        fig.savefig(GRAPH_FILENAME)  # save the figure to file
        plt.close(fig)  # close the figure



    def calculateBPS(self, count, usageDiff, timeDiff):
        bpsList = [] # Put our bits per second in list

        for x in range(0, count):
            dataSample = usageDiff[x]
            timePeriod = timeDiff[x]
            bitsPerSec = (dataSample / timePeriod)

            bpsList.append(bitsPerSec)

        return bpsList



graphingManager()


