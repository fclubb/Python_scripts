"""
This script creates plots of the number of streams of each order,
the mean length of each order, and the mean drop of each order.  It
takes as an input files created by stream_ordering_driver.cpp.

FJC 25/03/16

"""
#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy import stats
from glob import glob
from pylab import *


def make_plots():
    
    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 18

    ######################################
    #                                    #
    #   READ IN THE NUMBER OF STREAMS    #
    #                                    #
    ######################################

    DataDirectory =  './'    
    DEM_name = 'Coweeta_DEM'
    Plot_title = 'Coweeta, NC'
    FileName = 'Number_Streams_'+DEM_name+'.txt'
    OutputFigureName = 'stream_order_'+DEM_name
    OutputFigureFormat = 'png'
    f = open(DataDirectory + FileName,'r')  # open file
    lines = f.readlines()  # read in the data
    no_lines = len(lines)   # get the number of lines (=number of data)

    # data variables
    stream_order = np.zeros(no_lines)        # stream order
    count = np.zeros(no_lines)               # frequency

    for i in range (0,no_lines):
        line = lines[i].strip().split(" ")
        #print line
        stream_order[i] = int(line[0])
        count[i] = int(line[1])

    f.close()
    
    ###############################
    #                             #
    #   READ IN THE LENGTH DATA   #
    #                             #
    ###############################
   
    SO_lengths = np.zeros(no_lines)
    mean_lengths = np.zeros(no_lines)  
    j=0
    
    for FileName in glob(DataDirectory+"Lengths_Order*"+DEM_name+".txt"): 
        # Get the stream order of the file
        split_fname = FileName.split('_')     
        SO_lengths[j] = int(split_fname[2])
        
        # Open the file and read in the data
        f = open(DataDirectory + FileName, 'r')
        lines = f.readlines()
        no_lines2 = len(lines)
        
        lengths = np.zeros(no_lines2)
        for i in range (0, no_lines2):
            lengths[i] = float(lines[i].strip())
            
        mean_lengths[j] = np.mean(lengths)        
        print "SO:", SO_lengths[j], "Mean length:", mean_lengths[j]
        j=j+1
            
    #############################
    #                           #
    #   READ IN THE DROP DATA   #
    #                           #
    #############################
   
    SO_drops = np.zeros(no_lines)
    mean_drops = np.zeros(no_lines)  
    k=0
    
    for FileName in glob(DataDirectory+"Drops_Order*"+DEM_name+".txt"): 
        # Get the stream order of the file
        split_fname = FileName.split('_')   
        SO_drops[k] = int(split_fname[2])
        
        # Open the file and read in the data
        f = open(DataDirectory + FileName, 'r')
        lines = f.readlines()
        no_lines2 = len(lines)
        
        drops = np.zeros(no_lines2)
        for i in range (0, no_lines2):
            drops[i] = float(lines[i].strip())
            
        mean_drops[k] = np.mean(drops)        
        print "SO:", SO_drops[k], "Mean drop:", mean_drops[k]
        k=k+1   
           
    ###############################
    #                             #
    #       DO SOME ANALYSIS      #
    #                             #
    ###############################
        
    count_log = log10(count)
    gradient, intercept, r_value, p_value, st_err = stats.linregress(stream_order, count_log)
    print "Power law regression stats: Number of streams"
    print "Gradient:", gradient
    print "P value:", p_value
    print "R2:", r_value
    print "Standard error", st_err
    
    #intercept = 10**intercept
    print "Intercept", intercept
    x = np.linspace(0,max(stream_order),len(stream_order))
    y = 10**(gradient*x + intercept)
    
    length_log = log10(mean_lengths)
    gradient, intercept, r_value, p_value, st_err = stats.linregress(stream_order, length_log)
    print "Power law regression stats: Length of streams"
    print "Gradient:", gradient
    print "P value:", p_value
    print "R2:", r_value
    print "Standard error", st_err
    
    print "Intercept", intercept
    x2 = np.linspace(0,max(stream_order),len(stream_order))
    y2 = 10**(gradient*x2 + intercept)
       
    #################    
    #               #
    #   MAKE PLOTS  #
    #               #
    #################
    
    fig = plt.figure(1, facecolor='white', figsize=(21,7))
    
    ax = fig.add_subplot(131)
    subplots_adjust(wspace = 0.25)         
    plt.scatter(stream_order, count, c='r', s=100, zorder=100)
    plt.plot(x,y, 'k-.', lw=2)
    #plt.annotate('$R_B = 4.23$', (4,150), color='k', fontsize=20, transform=ax.transAxes, bbox=dict(facecolor='white', edgecolor='black', boxstyle='square, pad=0.3'))
    #plt.xlabel('Stream order, $\omega$')
    plt.ylabel('Log number of streams')
    ax.set_yscale('log')
    plt.xlim(0,max(stream_order)+1)  
    plt.ylim(0,max(y))
    
    ax2 = fig.add_subplot(132)
    plt.scatter(stream_order, mean_lengths, c='r', s=100, zorder=100)
    plt.plot(x2,y2, 'k-.', lw=2)
    plt.xlabel('Stream order, $\omega$')
    plt.ylabel('Log mean length (m)')
    plt.title(Plot_title)
    ax2.set_yscale('log')
    plt.xlim(0,max(stream_order)+1) 
    plt.ylim(0,max(mean_lengths)+10)
    
    ax3 = fig.add_subplot(133)
    plt.scatter(stream_order, mean_drops, c='r', s=100)
    plt.ylabel('Mean drop (m)')
    plt.xlim(0,max(stream_order)+1) 
    plt.ylim(0,max(mean_drops)+10)
    
    
    #plt.show()
    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat)
    plt.clf()
    
if __name__ == "__main__":
    make_plots()   
    
    
    
    
    
    
    
    
    
    
    
    
    
    