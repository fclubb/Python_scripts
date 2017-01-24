"""
Create a series of points at a specified distance along a line using shapely
FJC
24/01/17
"""

def get_points_along_line(DataDirectory, baseline_shapefile, distance):

    from fiona import collection
    from shapely.geometry import shape, Point, MultiLineString

    lines = []
    points = []
    # read in the baseline shapefile
    with collection(DataDirectory+baseline_shapefile, 'r') as input:
        for f in input:
            lines.append(MultiLineString(shape(f['geometry'])))
    #print line

    for line in lines:
        total_distance = line.length
        # handle exceptions
        if distance < 0.0 or distance >= total_distance:
            print "\tNot a valid distance, sorry pal!"

        # get the points at the specified distance along the line
        temp_distance = distance
        n_points = int(total_distance/distance)
        print "The total distance is", total_distance, ", returning ", n_points, "points"
        for j in range(n_points):
            point = line.interpolate(temp_distance)
            print point
            temp_distance+=distance



if __name__ == '__main__':

    DataDirectory = '/home/s0923330/Datastore/DEMs_for_analysis/eel_river/'
    #DataDirectory = 'Z:\\5m_dems\\scotland\\Catchment_boundaries\\'
    get_points_along_line(DataDirectory,baseline_shapefile='Eel_baseline.shp',distance=1)
