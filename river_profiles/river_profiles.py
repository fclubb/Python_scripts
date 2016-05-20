# -*- coding: utf-8 -*-
"""
Print river profiles

@author: s0923330
"""

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.colors as colors
import matplotlib.cm as cmx
from pylab import *
from scipy import stats
import matplotlib.ticker as plticker


def make_plots():
    
    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 14

    ###############################
    #                             #
    #   READ IN THE DATA CLOUD    #
    #                             #
    ###############################

    DataDirectory =  './'    
    FileName = 'inch_dem_137_chan.csv'
    OutputFigureName = 'inch_dem_loanan'
    OutputFigureFormat = 'png'
    f = open(DataDirectory + FileName,'r')  # open file
    lines = f.readlines()[1:]   # read in the data
    no_lines = len(lines)   # get the number of lines (=number of data)

    # data variables
    i_d = np.zeros(no_lines)        # drainage density
    x = np.zeros(no_lines)                # mean hilltop curvature
    y = np.zeros(no_lines)              # mean slope
    row = np.zeros(no_lines) 
    col = np.zeros(no_lines) 
    dist_from_outlet = np.zeros(no_lines) 
    dist_from_jn = np.zeros(no_lines) 
    elevation = np.zeros(no_lines) 
    drainage_area = np.zeros(no_lines)           # drainage area
    chi = np.zeros(no_lines)                       # marker size
    stream_power = np.zeros(no_lines)

  
    for i in range (0,no_lines):
        line = lines[i].strip().split(",")
        #print line
        i_d[i] = int(line[0])
        x[i] = int(line[1])
        y[i] = int(line[2])
        row[i] = int(line[3])
        col[i] = int(line[4])
        dist_from_outlet[i] = float(line[5])
        dist_from_jn[i] = float(line[6])
        elevation[i] = float(line[7])
        drainage_area[i] = float(line[8])
        chi[i] = float(line[9])
        
    f.close()
    
    dist_from_jn_km = dist_from_jn/1000
    
    #################    
    #               #
    #   MAKE PLOTS  #
    #               #
    #################
    
    fig = plt.figure(1, facecolor='white', figsize=(10,5))
    
    ax = fig.add_subplot(111)
    plt.grid(b=True, which='major', color='0.65',linestyle='-', lw=1.2)
    #plt.grid(b=True, which='minor', color='0.65',linestyle='-')
    #subplots_adjust(left = 0.2)         
    plt.plot(dist_from_jn_km, elevation, 'k-', zorder = 100)
    plt.xlabel('Distance upstream from Loch Assynt (km)')
    plt.ylabel('Elevation (m)')
    plt.title('Loanan')
    plt.xlim(0,12)  
    plt.ylim(0,400)
    #plt.xticks(np.arange(min(dist_from_jn_km), 11, 1.0))
    #plt.show()
    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat)
    plt.clf()
    
if __name__ == "__main__":
    make_plots()   
    
    
    
    
    
    
    
    
    
    
    
    
    
    