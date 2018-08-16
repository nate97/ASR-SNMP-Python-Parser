import datetime
import time
import os

import matplotlib.pyplot as plt
from matplotlib import cycler
import numpy as np



class usageGraphic():

    def __init__(self):

        self.test()
        print ("Graphing")

        
        

        with plt.style.context('ggplot'):
            self.test()


        


    def test(self):

        np.random.seed(0)
        fig, ax = plt.subplots(1, 2, figsize=(11, 4))

        print (np.random.randn(1000))
        ax[0].hist(np.random.randn(1000))


        fig.savefig('to.png')  # save the figure to file

usageGraphic()