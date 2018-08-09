import datetime
import time
import os

import matplotlib.pyplot as plt



class usageGraphic():

    def __init__(self):

        self.test()
        print ("Graphing")



    def test(self):

        fig, ax = plt.subplots(nrows=1, ncols=1)  # create figure & 1 axis
        ax.plot([1, 2, 3, 4, 5, 6], [10, 20, 10, 5, 5, 5])
        fig.savefig('to.png')  # save the figure to file
        plt.close(fig)  # close the figure


usageGraphic()