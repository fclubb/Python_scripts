"""
make_hydrograph.py

This script reads in the catchment data generated from LSDCatchmentModel and creates
a plot of the discharge at the outlet of the catchment against the duration of the
storm.  The flood hydrograph can be used to select the timestep at which the discharge 
at the outlet was the greatest.

Fiona Clubb
20/05/16
"""
#import modules
import numpy as np, matplotlib.pyplot as plt
    
def make_hydrograph(field_site, duration, plot_title, return_period):
    """
    Makes plot of the flood hydrograph from LSDCatchmentModel
    
    """
    #import modules
    from glob import glob
    from matplotlib import rcParams
    import operator
    
    # Set up fonts
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 12
    
    # Read in the data
    DataDirectory = './'
    FileName = field_site+'_catchment_'+str(duration)+'hr_'+str(return_period)+'yr.dat'
    f = open(DataDirectory+FileName, 'r')
    lines = f.readlines()
    no_lines = len(lines)
    
    # Declare the arrays for the variables
    time_step = np.zeros(no_lines)
    discharge = np.zeros(no_lines)    
    
    for i in range (no_lines):
        line = lines[i].strip().split(' ')
        time_step[i] = int(line[0])
        discharge[i] = float(line[2])
            
    # Now make the plot
    fig = plt.figure(1, facecolor='white', figsize=(7,5))
    
    ax = fig.add_subplot(111)
    ax.plot(time_step, discharge, lw=2)
        
    ax.set_xlabel('Time (hours)', fontsize=14)
    ax.set_ylabel('Discharge at outlet (m$^3$/s)', fontsize=14)
    ax.set_title(plot_title)
    
    # Save figure
    OutputFigureName = field_site+'_flood_hydrograph_'+str(duration)+'hr_'+str(return_period)+'yr'
    OutputFigureFormat = 'pdf'
    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat)
    
    index, value = max(enumerate(discharge), key=operator.itemgetter(1))
    print 'Maximum discharge is', value, 'cumecs at', time_step[index], 'hours'
   
if __name__ == "__main__":
    
    # Set the name of the field site
    field_site = 'swale'
    plot_title = 'River Swale, UK'
    
    # Set the duration of the storm
    duration = 6
    
    # Set the return period
    return_period = 100
    
    make_hydrograph(field_site, duration, plot_title, return_period)


