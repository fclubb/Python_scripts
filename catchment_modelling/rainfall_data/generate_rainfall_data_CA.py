"""
generate_rainfall_data.py
WORKS WITH NOAA Atlas 14 Volume 6: California Region 7

This script takes in a csv file with the temporal distribution of rainfall
for a given storm duration for a site downloaded from the NOAA Precipitation
Data Frequency Server: http://hdsc.nws.noaa.gov/hdsc/pfds/index.html
The median "all cases" distribution is used.
It also takes the precipitation depth for the given duration, along with the 
upper and lower bounds of the 90% confidence interval.  It generates
a hypothetical rainfall distribution for a storm event with a 100-year 
return period, and a duration specified by the temporal distribution file.

The rainfall distribution is stored as a text file.  It also generates a plot
of the distribution through time.

Once the inital storm data is calculated there is the option to add rainfall data
for preceding/following days to simulate the antecedent conditions.

Fiona Clubb
06/05/16
"""
#import modules
import numpy as np, matplotlib.pyplot as plt
import re

numbers = re.compile(r'(\d+)')

def numericalSort(value):
    """
    Sorter for reading filenames in numerical order
    
    """
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def generate_storm_data(field_site, duration, pcp_depth, upper_bound, lower_bound):
    
    """
    Generate the storm data for the field site with a given storm duration and total
    precipitation depth
    
    """
          
    # Read in the csv file with the temporal distribution for the field site
    DataDirectory =  './'    
    FileName = 'Temporal_distributions_'+str(duration)+'_hr.csv'
    f = open(DataDirectory + FileName,'r')  # open file
    print "Duration:", duration
    
    # Read in the data: different file format for each duration file
    if (duration == 6):
        lines = f.readlines()[80:]   # read in the data: use the distribution for "all cases"
    elif (duration == 12):
        lines = f.readlines()[128:]   # read in the data: use the distribution for "all cases"
    elif (duration == 24):
        lines = f.readlines()[224:]   # read in the data: use the distribution for "all cases"
    elif (duration == 96):
        lines = f.readlines()[416:]   # read in the data: use the distribution for "all cases"
    else:   # bounds checking
        print "WARNING: your storm duration does not correspond to one of the temporal distribution files. Please use a different duration."
    
    no_lines = len(lines)
    # Make arrays with data variables
    percent_pcp = np.zeros(no_lines)        # percent of total precipitaiton 
    storm_duration = np.zeros(no_lines)     # duration in hours
    pcp = np.zeros(no_lines)                # precipitation in mm
    pcp_upper = np.zeros(no_lines)          # upper bound of pcp (90% confidence)
    pcp_lower = np.zeros(no_lines)          # lower bound of pcp (90% confidence)
    hourly_pcp = np.zeros(duration+1)                   # hourly precipitation in mm
    hourly_pcp_upper = np.zeros(duration+1)                # upper bound of hourly pcp (90% confidence)
    hourly_pcp_lower = np.zeros(duration+1)                # lower bound of hourly pcp (90% confidence)
    
    # Get the data from the file
    #print len(lines)
    #print lines
    for i in range (0, no_lines):
        line = lines[i].strip().split(",")
        storm_duration[i] = float(line[0])
        percent_pcp[i] = float(line[5])
        #if (storm_duration[i] == duration):
        #    break

    
    # Convert percent pcp into precipitation in mm given total rainfall depth
    j = 0
    for i in range(0, len(percent_pcp)):
        if (i == 0):
            pcp[j] = 0
            pcp_upper[j] = 0
            pcp_lower[j] = 0
            j = j+1
        else:
            pcp[j] = ((percent_pcp[i] - percent_pcp[i-1])*pcp_depth)/100
            pcp_upper[j] = ((percent_pcp[i] - percent_pcp[i-1])*upper_bound)/100
            pcp_lower[j] = ((percent_pcp[i] - percent_pcp[i-1])*lower_bound)/100
            j = j+1

    print 'Duration', storm_duration    
    print 'Precipitation', pcp
    
    # Convert precipitation in mm into hourly precipitation
    if (duration == 96):
        # 96 hour storm: take every measurement from the array
        hourly_pcp = pcp
        hourly_pcp_upper = pcp_upper
        hourly_pcp_lower = pcp_lower
    
    else:
        j = 0
        # 6, 12 or 24 hour storm: take every 2nd measurement from the array
        for i in range (0, len(pcp)):
            if (i%2 == 0):
                if (i == 0):
                    hourly_pcp[j] = 0
                    hourly_pcp_upper[j] = 0
                    hourly_pcp_lower[j] = 0
                    j = j+1
                else:
                    hourly_pcp[j] = pcp[i]+pcp[i-1]
                    hourly_pcp_upper[j] = pcp_upper[i]+pcp[i-1]
                    hourly_pcp_lower[j] = pcp_lower[i]+pcp[i-1]
                    j = j+1

    # checking        
    print ' Hourly pcp', hourly_pcp
    print 'Sum hourly pcp:', sum(hourly_pcp), 'Total pcp depth:', pcp_depth
    
    # Make plot of hourly rainfall through time
    hourly_duration = list(range(duration+1))
    plt.plot(hourly_duration, hourly_pcp)
    plt.plot(hourly_duration, hourly_pcp_upper, 'k--', label='90% confidence interval')
    plt.plot(hourly_duration, hourly_pcp_lower, 'k--')
    plt.legend(loc=1, bbox_to_anchor=(1.05,1.05))
    plt.xlabel('Storm duration (hours)')
    plt.ylabel('Precipitation (mm)')
    #plt.show()
    
    # Save figure
    OutputFigureName = field_site+'_rainfall_'+str(duration)+'_hr'
    OutputFigureFormat = 'png'
    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat)
    plt.clf()
    
    # Generate text file with rainfall data
    OutputFileName = field_site+'_rainfall_data_'+str(duration)+'_hr.txt'
    out_file = open(DataDirectory + OutputFileName,'w')  # open file
    for i in range(0,len(hourly_pcp)):
        out_file.write(str(hourly_pcp[i])+'\n')
    
    out_file.close()
    
def add_surrounding_conditions(field_site, duration, n_preceding_hours, n_following_hours,
                               preceding_pcp_rate, following_pcp_rate):
    
    """
    Add rainfall data for hours preceding and following the storm event
    
    """
    # Load the text file with the storm rainfall data
    DataDirectory =  './'    
    FileName = field_site+'_rainfall_data_'+str(duration)+'_hr.txt'
    f = open(DataDirectory + FileName,'r')  # open file
    lines = f.readlines()
    no_lines = len(lines)
    
    # Declare arrays for data variables
    storm_pcp = np.zeros(no_lines-1)
    preceding_pcp = np.empty(n_preceding_hours)
    following_pcp = np.empty(n_following_hours)
    
    # Get the data for the storm precipitation
    for i in range(1, no_lines):
        line = lines[i].strip()
        storm_pcp[i-1] = line
    
    # Add the data for preceding and following hours
    preceding_pcp.fill(preceding_pcp_rate)
    following_pcp.fill(following_pcp_rate)
    
    # Make the new file with the additional data
    total_rain_duration = no_lines + n_preceding_hours + n_following_hours
    print "Total rain duration:", total_rain_duration
    print total_rain_duration-n_following_hours
    
    OutputFileName = field_site+'_rainfall_data_all_'+str(duration)+'_hr.txt'
    out_file = open(DataDirectory + OutputFileName,'w')  # open file
    
    for i in range(0, n_preceding_hours):
        out_file.write(str(preceding_pcp[i])+'\n')
    
    j=0
    for i in range(n_preceding_hours+1, (total_rain_duration-n_following_hours)):
        out_file.write(str(storm_pcp[j])+'\n')
        j=j+1
    
    j=0        
    for i in range((total_rain_duration-n_following_hours+1), total_rain_duration+1):
        out_file.write(str(following_pcp[j])+'\n')
        j=j+1
    

    out_file.close()
    
def make_rainfall_plots(field_site, plot_title):
    """
    Make nice subplots of the rainfall distributions for each storm duration
    
    """
    #import modules
    from glob import glob
    from matplotlib import rcParams
    
    # Set up fonts
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 12
    
    # Read in the files sorted by duration
    DataDirectory = './'
    FileList = sorted(glob(DataDirectory+field_site+'_rainfall_data_all*'), key=numericalSort)
      
    n_files = len(FileList)
    print "Number of files = ", n_files
    
    #Declare the array of arrays
    pcp_all = []
    duration_all = []
    
    FileNo = 0
    for FileName in FileList:
        print "This file name is: ", FileName
        
        # Read in the file
        f = open(FileName, 'r') 
        lines = f.readlines()
        no_lines = len(lines)
        
        # Declare the arrays for the variables
        pcp = np.zeros(no_lines)
        duration = np.zeros(no_lines)
        
        # Populate the arrays with the pcp data
        hour = 1
        for i in range(len(lines)):
            pcp[i] = lines[i].strip()
            duration[i] = hour
            hour = hour+1
        
        # Now populate the array of arrays
        pcp_all.append(pcp)
        duration_all.append(duration)
        FileNo = FileNo+1
      
    # Now make the subplots
    fig, ax = plt.subplots(2,2, figsize=(7, 6))
    plt.subplots_adjust(wspace = 0.3, hspace=0.3)
    
    ax = ax.ravel()
    
    for i in range (n_files):
        #plot the data
        ax[i].plot(duration_all[i], pcp_all[i], lw=2)
        
        #add duration to the top corner of the plot
        FileName = FileList[i].strip().split('_')
        duration = str(FileName[5])
        ax[i].text(0.7, 0.8, (duration+' hour\nstorm'), transform=ax[i].transAxes)
        
        
    # Add a big subplot to get a common x and y label for the subplots
    fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axes
    plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
        
    plt.xlabel('Time (hours)', fontsize=14)
    plt.ylabel('Precipitation (mm)', fontsize=14)
    plt.title(plot_title, y = 1.05)
    
    # Save figure
    OutputFigureName = field_site+'_rainfall_all_durations'
    OutputFigureFormat = 'pdf'
    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat)
   
if __name__ == "__main__":
    
    # Set the name of the field site
    field_site = 'russian_river'
    plot_title = 'Russian River, California'
    
    # Set the duration of the storm
    duration = 96
#    
#    # Set the total precipitation to fall during the storm (mm)
#    pcp_depth = 435
#    upper_bound = 537
#    lower_bound = 359
#    
#    generate_storm_data(field_site, duration, pcp_depth, upper_bound, lower_bound) 
    
    # Set the duration for preceding/following hours
    n_preceding_hours = 48
    n_following_hours = 48
    
    # Set the precipitation rates in mm per hour
    preceding_pcp_rate = 0.5 
    following_pcp_rate = 0.0 
    
    #add_surrounding_conditions(field_site, duration, n_preceding_hours, n_following_hours,
    #                           preceding_pcp_rate, following_pcp_rate)
    
    make_rainfall_plots(field_site, plot_title)


