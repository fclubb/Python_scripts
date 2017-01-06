#-----------------------------------------------------------------------------#
# Manipulate_shapefiles.py
# Contains functions to manipulate shapefiles
# FJC 06/01/17
#-----------------------------------------------------------------------------#

import csv
from shapely.geometry import Point, mapping
from fiona import collection

def write_points_from_csv(DataDirectory, csv_file, output_shp):
    """
    This function takes a csv file with a list of coordinates and writes a 
    shapefile of points
    Needs to have the columns: ID, x, y
    """
    # Define the features and their properites
    schema = { 'geometry': 'Point', 'properties': { 'ID': 'str' } }
    
    # use fiona to write the shapefile
    with collection(DataDirectory+output_shp, "w", "ESRI Shapefile", schema) as output:
        # open the csv file and read in the points
        with open(DataDirectory+csv_file, 'rb') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # for each row, define the point using x and y coords
                point = Point(float(row['x']), float(row['y']))
                # write properties
                output.write({
                    'properties': {
                        'ID' : row['ID']
                        },
                        'geometry': mapping(point)
                    })
            
            
DataDirectory = "Z:\\DEMs_for_analysis\\mid_bailey_run\\"
csv_file = "Bailey_FIPs.csv"
output_shp = "Bailey_FIPs.shp"
write_points_from_csv(DataDirectory, csv_file, output_shp)