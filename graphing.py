import matplotlib.pyplot as plt
import numpy as np

import datetime
import os


# GLOBALS #



class graphingManager():

    def __init__(self):
        print ("Graphing")



    def graphPrerequisites(self, customerList):

        timeSeconds = []
        outUsage = []
        timeL = []

        firstSample = True

        print (customerList)
        for uu in customerList[10]:
            print (uu)
            outOctet = (int(uu[1]))
            outOctet = self.octetToMb(outOctet)
            time = (float(uu[2]))

            outUsage.append(outOctet)

            if not firstSample:
                # Visual data, this is what we draw on the png file for the time scale
                timeStr = datetime.datetime.fromtimestamp(time).strftime('%H:%M')
                timeL.append(timeStr)

            # Seconds
            timeSeconds.append(time)
            firstSample = False

        outUsageDiff = [outUsage[i + 1] - outUsage[i] for i in range(len(outUsage) - 1)]
        timeDiff = [timeSeconds[i + 1] - timeSeconds[i] for i in range(len(timeSeconds) - 1)]

        sortedUsageDiff = sorted(outUsageDiff)

        length = len(sortedUsageDiff)


graphingManager()


