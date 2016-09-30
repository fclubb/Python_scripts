## make_frequency_plot.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## FJC 30/09/16
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
#import matplotlib as mpl
#import matplotlib.cm as cmx
#from pylab import *

def cm2inch(value):
    return value/2.54

def make_plots(InputFileName, OutputFigureName, OutputFigureFormat):
    

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 10
    
    # Read in the data

    DataDirectory =  './'    
    f = open(DataDirectory + InputFileName,'r')  # open file
    lines = f.readlines()[1:]   # read in the data
    no_lines = len(lines)   # get the number of lines (=number of data)

    # data variables
    row = np.zeros(no_lines)        # midpoint of each bin
    col = np.zeros(no_lines)       # lower limit
    raster_data = np.zeros(no_lines)       # upper limit
    
    print len(raster_data)

    for i in range (0,no_lines):
        line = lines[i].strip().split(" ")
        #print line
        row[i] = int(line[0])
        col[i] = int(line[1])
        raster_data[i] = float(line[2])
        
    f.close()
        
    fig = plt.figure(1, facecolor='white', figsize=(cm2inch(12),cm2inch(8))) 
    ax = fig.add_subplot(111)
    plt.subplots_adjust(left=0.2, bottom = 0.2)
    
    ax.hist(raster_data, bins = 100)
    ax.set_xlabel('Channel relief (m)')
    ax.set_ylabel('Frequency')
    
    #xlocs, xlabels = plt.xticks()
    #ax.set_xticklabels(xlabels, rotation=30)

    #plt.show()
    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat)
    #plt.clf()
    
    
if __name__ == "__main__":
    
    InputFileName = "Coweeta_DEM_channel_relief.txt"
    OutputFigureName = "Coweeta_DEM_relief_plot"
    OutputFigureFormat = "pdf"
    make_plots(InputFileName, OutputFigureName, OutputFigureFormat)    

	