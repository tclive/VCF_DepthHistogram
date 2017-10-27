from tkinter import *
from TermProject.vaginalis import Vaginalis
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


class GUI:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.button = Button(frame,
                             text="QUIT", fg="red",
                             command=frame.quit)
        self.button.pack(side=LEFT)
        self.slogan = Button(frame,
                             text="Crunch data",
                             command=self.displaydata)
        self.slogan.pack(side=LEFT)

        self.textBox = Entry(frame)
        self.textBox.pack()

    def displaydata(self):
        filename = "tvaginalis.seven_libs.bwa_mem.UG.vcf"  # 50143.bwa_mem.haplotype_caller.gvc

        factor = 1
        identifier = "test1"

        test_genome = Vaginalis(factor, identifier, filename)
        test_genome.parsefile(test_genome._dataFileName)

        # example data
        mu = test_genome.get_average_depth()  # mean of distribution
        # mu = 999
        # x = mu + np.random.randn(10000)
        x = np.asarray(test_genome.get_depths())

        num_bins = 50
        # the histogram of the data
        n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
        # add a 'best fit' line
        y = mlab.normpdf(bins, mu, 1)
        plt.plot(bins, y, 'r--')
        plt.xlabel('Depth')
        plt.ylabel('Occurrence')
        plt.title(r'Histogram of IQ: $\mu= %d $' % mu)

        # Tweak spacing to prevent clipping of ylabel
        plt.subplots_adjust(left=0.15)
        plt.show()
        print("reading is done")


root = Tk()
app = GUI(root)
root.mainloop()