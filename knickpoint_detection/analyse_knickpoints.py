## analyse_knickpoints.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This scripts takes in the Mchi files with the knickpoint information
## and creates various plots.  User specifies a threshold knickpoint magnitude
## (difference in MChi between the upstream and downstream segments)
## MChi file is read in using pandas
##
## 1. For each basin, it looks at the relationship between the flow distance
## (distance from the basin outlet) and the elevation of the knickpoints
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## Authors: BG, FJC
## 29/03/17
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#set backend to run on server
import matplotlib
matplotlib.use('Agg')

#import modules
from matplotlib import pyplot as plt
import numpy as np
import os
import matplotlib
import pandas

def read_MChi_file(DataDirectory, csv_name, kp_threshold):
    """
    This function reads in the MChi file using pandas
    file structure:
    latitude	longitude chi	elevation	flow distance	drainage area	m_chi	b_chi	source_key	basin_key	segmented_elevation	knickpoints	knickpoint_sign	segment_length	file_from_combine
    FJC 29/03/17
    """
    df = pandas.read_csv(DataDirectory+csv_name, sep=",")
    df = df[df.knickpoints >= kp_threshold]
    return df

def get_data_columns_from_csv(DataDirectory, csv_name, kp_threshold, columns):
    """
    This function returns lists of specified column names from the MChi csv file.
    Must be strings equal to the column headers.
    User can specify a knickpoint threshold (values with knickpoint magnitudes
    below this will be excluded)
    FJC 29/03/17
    """
    column_lists = [[]]
    df = read_MChi_file(DataDirectory, csv_name, kp_threshold)
    for column_name in columns:
        print("I'm returning the "+column_name+" values as a list")
        column_values = list(df[column_name])
        column_lists.append(column_values)
    return column_lists

def make_cumulative_plot(DataDirectory, csv_name, kp_threshold):
    print("Now printing the cumulative plot")
    sorted_data = read_MChi_file(DataDirectory, csv_name, kp_threshold)
    temp_count = 0
    x_cumul, y_cumul = np.unique(sorted_data[:,11],return_counts= True)
    #y_cumul = np.unique(sorted_data[:,11],return_counts= True)
    for i in range(1,x_cumul.size):
        y_cumul[i] = y_cumul[i]+y_cumul[i-1]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_cumul, y_cumul, 'k--', linewidth=1)

    print("Saving the Cumulative plot")
    # tidy up the figure
    ax.grid(True)
    ax.set_title('Cumulative step histograms')
    ax.set_xlabel('kinckpoint value')
    ax.set_ylabel('Cumulative %')
    #ax.set_ylim(0,100)
    ax.set_xlim(0,sorted_data[:,11].max())
    write_name = "kp_cumulative"
    file_ext = "png"
    plt.savefig(DataDirectory+write_name+"."+file_ext,dpi=300)
    plt.clf()

    #### Elevation against Knickpoints ####
def plot_knickpoint_elevations(DataDirectory, csv_name, kp_threshold):
    """
    This function creates a plot of knickpoint elevations against magnitude
    FJC 29/03/17, modified from code by BG.
    """
    # read in the data from the csv to lists
    elevation = get_data_column_from_csv(DataDirectory, csv_name, kp_threshold, "elevation")
    kp_magnitude = get_data_column_from_csv(DataDirectory, csv_name, kp_threshold, "knickpoints")

    # plot the figure
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(kp_magnitude, elevation, 'k+', linewidth=0.5)
    ax.grid(True)
    ax.set_title('Elevation against knickpoint value')
    ax.set_xlabel('Knickpoint magnitude')
    ax.set_ylabel('Elevation (m)')
    #ax.set_ylim(0,100)
    ax.set_xlim(0,1000)
    write_name = "knickpoint_elevation"
    file_ext = "png"
    plt.savefig(DataDirectory+write_name+"."+file_ext,dpi=300)
    plt.clf()

def plot_elevation_distance(DataDirectory, csv_name, kp_threshold):
    """
    This function creates a plot of knickpoint elevations against distance from the outlet
    of the basin.  Creates a separate plot for each basin at the moment.
    FJC 29/03/17
    """
    # read in data from the csv to lists
    columns = ["elevation", "flow distance", "file_from_combine"]
    column_lists = get_data_columns_from_csv(DataDirectory, csv_name, kp_threshold, columns)
    # elevation = column_lists[0]
    # flow_distance = column_lists[1]
    basin_id = column_lists[2]
    #list_of_lists = zip(elevation,flow_distance,basin_id)
    print column_lists

    # loop through and get a plot for each basin id
    ids = set(basin_id)
    for id in ids:
        print("This basin id is: "+str(id))
        these_lists = [(x,y,z) for (x,y,z) in column_lists if z == id]
        print these_lists


DataDirectory = '/home/s0923330/LSDTopoData/Sierra_Nevada_kn/'
baseName = "combined"
csv_name = baseName + "_MChi.csv"
kp_threshold = 25 # every knickpoint below this will be erased
plot_elevation_distance(DataDirectory,csv_name, kp_threshold)
#get_data_column_from_csv(DataDirectory,csv_name,kp_threshold,column_name="latitude")
