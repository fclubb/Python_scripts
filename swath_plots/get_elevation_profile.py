"""
get_elevation_profile.py

This script takes in a csv file with the mean, min and max elevation along a swath profile

Fiona Clubb
19/10/16
"""

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.cm as cmx
#import seaborn as sns
import matplotlib.colors as colors
#from rand_cmap import rand_cmap
from matplotlib import gridspec
#from adjustText import adjust_text

def cm2inch(value):
    return value/2.54

def read_all_data(DataDirectory,DEM_prefix):
    """
    Read in the data with all the points

    """

    # read in the file
    FileName = DEM_prefix+'_swath_elevations.csv'
    f = open(DataDirectory + FileName,'r')  # open file
    lines = f.readlines()[1:]   # read in the data
    no_lines = len(lines)   # get the number of lines (=number of data)
    print "Number of lines: ", no_lines

    # Set up the arrays
    distance = []
    MeanValues = []
    MinValues = []
    MaxValues = []

    for i in range (no_lines):
        line = lines[i].strip().split(",")
        if np.isnan(float(line[1])) == False:
            distance.append(float(line[0]))
            MeanValues.append(float(line[1]))
            MinValues.append(float(line[2]))
            MaxValues.append(float(line[3]))

    return distance, MeanValues, MinValues, MaxValues

def make_elevation_plots(DataDirectory,DEM_prefix,field_site):
    """
    Make nice plots of the elevations along the swath

    """

    # Set up fonts
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 14

    distance, MeanValues, MinValues, MaxValues = read_all_data(DataDirectory, DEM_prefix)

    # add the XY Plot
    fig = plt.figure(1, figsize=(cm2inch(25),cm2inch(15)))
    # set ratios for subplots
    ax = fig.add_subplot(111)
    ax.plot(distance, MeanValues, 'r', lw=2, label = "Mean")
    ax.plot(distance, MinValues, 'k--', lw=1, label = "Max/min")
    ax.plot(distance, MaxValues, 'k--', lw=1)
    plt.xlabel('Distance along swath (m)')
    plt.ylabel('Elevation (m)')
    plt.ylim(150,400)
    plt.title(field_site)
    plt.legend(loc='upper right')

    # Save figure
    OutputFigureName = DEM_prefix+'_elevation_plots'
    OutputFigureFormat = 'png'
    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat, dpi=300)
    #plt.tight_layout()
    plt.close()

if __name__ == "__main__":

    DEM_prefix = 'bailey_dem_10m'
    field_site = "Mid Bailey Run swath profile"
    #DataDirectory = 'Z:\\DEMs_for_analysis\\eel_river\\'
    DataDirectory = '/home/s0923330/Datastore/DEMs_for_analysis/mid_bailey_run_10m/'
    make_elevation_plots(DataDirectory, DEM_prefix, field_site)
