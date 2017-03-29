from matplotlib import pyplot as plt
import numpy as np
import os
import matplotlib
import pandas

# Param for saving
rDirectory = "your/path"
baseName = "combined"
fname = baseName + "_MChi.csv"
cutoff = 25 # every knickpoint below this will be erased
print_cumululative_plot = True
print_Elevation_knickpoints = True

df = pandas.read_csv(rDirectory + fname, sep=",")
data = np.array(df.values) # Raw values
sorted_data = data[data[:,11]>cutoff] # Sorted values
## file structure
#latitude	longitude chi	elevation	flow distance	drainage area	m_chi	b_chi	source_key	basin_key	segmented_elevation	knickpoints	knickpoint_sign	segment_length	file_from_combine


########################## Ok Below this I tried some stuffs, I don't remember the result, feel free to erase it must be shit, regards, Boris. ##############################
if(print_cumululative_plot):
    print("Now printing the cumulative plot")
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
    plt.savefig(wDirectory+wname+"_Cumulative"+ext,dpi=pdpi)
    plt.clf()


    #### Elevation against Knickpoints ####
if(print_Elevation_knickpoints):

    elevation = sorted_data[:,3]
    knickpoint_value = sorted_data[:,11]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(knickpoint_value, elevation, 'k+', linewidth=0.5)
    ax.grid(True)
    ax.set_title('Elevation against knickpoint value')
    ax.set_xlabel('Knickpoint magnitude')
    ax.set_ylabel('Elevation (m)')
    #ax.set_ylim(0,100)
    ax.set_xlim(0,1000)
    plt.savefig(wDirectory+wname+"_knickpoint_elevation"+ext,dpi=pdpi)
    plt.clf()
