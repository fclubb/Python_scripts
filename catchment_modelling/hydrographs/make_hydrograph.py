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
    
def make_hydrograph(field_site, duration):
    """
    Makes plot of the flood hydrograph from LSDCatchmentModel
    
    """
    #import modules
    from glob import glob
    from matplotlib import rcParams
    
    # Set up fonts
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 12
    
    # Read in the data
    DataDirectory = './'
    FileName = field_site+'_catchment_'+str(duration)+'hr.dat'
    f = open(DataDirectory+FileName, 'r')
    lines = f.readlines()
    no_lines = len(lines)
    
    # Declare the arrays for the variables
    time_step = np.zeros(no_lines)
    discharge = np.zeros(no_lines)    
    
    for i in range (no_lines):
        line = lines.strip().split(' ')
        time_step[i] = int(line[0])
        discharge[i] = float(line[1])
        
    #convert the discharge to mm
    discharge_mm = discharge*1000
    
    # Now make the plot
    fig = plt.figure(1, facecolor='white', figsize=(7,5))
    
    ax = fig.add_suplot(111)
    ax.plot(time_step, discharge_mm, lw=2)
        
    ax.set_xlabel('Time (hours)', fontsize=14)
    ax.set_ylabel('Discharge at outlet (mm)', fontsize=14)
    
    # Save figure
    OutputFigureName = field_site+'_flood_hydrograph_'+str(duration)+'hr'
    OutputFigureFormat = 'pdf'
    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat)
   
if __name__ == "__main__":
    
    # Set the name of the field site
    field_site = 'mid_bailey_run'
    
    # Set the duration of the storm
    duration = 6
    
    make_hydrograph(field_site, duration)


