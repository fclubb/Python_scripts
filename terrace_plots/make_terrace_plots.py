"""
make_terrace_plots.py

This script takes in a text file with the the distance of each terrace pixel
upstream along the main channel against the elevation compared to the main channel.

Fiona Clubb
19/10/16
"""

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.cm as cmx
import seaborn as sns
import matplotlib.colors as colors
from rand_cmap import rand_cmap
from adjustText import adjust_text

def cm2inch(value):
    return value/2.54

def read_all_data(DataDirectory,DEM_prefix):
    """
    Read in the data with all the points

    """

    # read in the file
    FileName = DEM_prefix+'_terrace_swath_plots.txt'
    f = open(DataDirectory + FileName,'r')  # open file
    lines = f.readlines()   # read in the data
    no_lines = len(lines)   # get the number of lines (=number of data)
    print "Number of lines: ", no_lines

    # Set up the arrays
    patch_id = np.zeros(no_lines)             # patch_id
    upstream_distance = np.zeros(no_lines)    # distance upstream
    channel_relief = np.zeros(no_lines)       # channel relief

    for i in range (no_lines):
        line = lines[i].strip().split(" ")
        if np.isnan(float(line[1])) == False:
            patch_id[i] = int(line[0])
            channel_relief[i] = float(line[1])
            upstream_distance[i] = float(line[2])

    upstream_distance = upstream_distance/1000
    return patch_id, upstream_distance, channel_relief

def read_binned_data(DataDirectory,DEM_prefix):
    """
    Read in the binned data

    """
    # read in the file
    FileName = DEM_prefix+'_terraces_data_binned.txt'
    f = open(DataDirectory + FileName,'r')  # open file
    lines = f.readlines()   # read in the data
    no_lines = len(lines)   # get the number of lines (=number of data)
    print "Number of lines: ", no_lines

    # Set up the arrays
    mean_distance = np.zeros(no_lines)    # distance upstream
    stdev_distance = np.zeros(no_lines)
    sterr_distance = np.zeros(no_lines)
    mean_relief = np.zeros(no_lines)       # channel relief
    stdev_relief = np.zeros(no_lines)
    sterr_relief = np.zeros(no_lines)


    for i in range (no_lines):
        line = lines[i].strip().split(" ")
        mean_distance[i] = line[0]
        stdev_distance[i] = line[1]
        sterr_distance[i] = line[2]
        mean_relief[i] = line[3]
        stdev_relief[i] = line[4]
        sterr_relief[i] = line[5]

    mean_distance = mean_distance/1000
    stdev_distance = stdev_distance/1000
    sterr_distance = sterr_distance/1000
    return mean_distance, stdev_distance, sterr_distance, mean_relief, stdev_relief, sterr_relief

def make_terrace_plots(DataDirectory,DEM_prefix,field_site):
    """
    Make nice plots of the upstream distance and channel relief

    """

    # Set up fonts
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 10

    patch_id, upstream_distance, channel_relief = read_all_data(DataDirectory, DEM_prefix)
    #mean_distance, stdev_distance, sterr_distance, mean_relief, stdev_relief, sterr_relief = read_binned_data(DataDirectory,DEM_prefix)

#    n_points = len(mean_relief)
#    terrace_levels = np.zeros(n_points)
#    # separate into levels for plotting colours
#    for i in range (n_points):
#        if mean_relief[i]

    new_cmap = rand_cmap(len(patch_id),type='bright',first_color_black=False,last_color_black=False,verbose=False)
    # make plots
    #sns.set_palette("Paired", 4)
    fig = plt.figure(1, facecolor='white', figsize=(cm2inch(22),cm2inch(12)))
    ax = fig.add_subplot(111)
    ax.scatter(upstream_distance, channel_relief, s=20, c=patch_id, cmap=new_cmap, lw=0.5)
    #plt.errorbar(mean_distance, mean_relief, xerr=stdev_distance, yerr=stdev_relief, fmt='None', ecolor='0.5', elinewidth=1, markersize=3, capsize=1)
    #plt.scatter(mean_distance, mean_relief, c=mean_relief, cmap=cmx.Blues)
    plt.xlabel('Distance upstream along main stem (km)')
    plt.ylabel('Elevation compared to main stem (m)')
    plt.xlim(0,np.max(upstream_distance)+1)
    plt.ylim(0,50)
    plt.title(field_site)
    # add labels for the catchment IDs
    labels = [str(int(x)) for x in patch_id]
    print labels
    for label, x, y in zip(labels,upstream_distance,channel_relief):
        texts = ax.text(x,y,label)
    adjust_text(texts, force_text=0.05)


    # Save figure
    OutputFigureName = DEM_prefix+'_xy_plots'
    OutputFigureFormat = 'png'
    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat, dpi=300)
    plt.close()

if __name__ == "__main__":

    DEM_prefix = 'Eel_DEM_clip'
    field_site = "Eel River, CA"
    #DataDirectory = 'Z:\\DEMs_for_analysis\\eel_river\\'
    DataDirectory = '/home/s0923330/Datastore/DEMs_for_analysis/eel_river/'
    make_terrace_plots(DataDirectory, DEM_prefix, field_site)
