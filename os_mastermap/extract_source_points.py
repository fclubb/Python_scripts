"""
Create a CSV file of source points from the OS MasterMap Water Network
Layer for each catchment in Scotland using  and shapely
FJC
30/01/17
"""

def extract_source_points(DataDirectory, catchment_shapefile, points_shapefile):

    from fiona import collection
    from shapely.geometry import shape, Polygon, Point
    import csv
    from matplotlib import pyplot as plt
    from operator import itemgetter

    shapes = []
    catchment_ids = []
    # read in the catchment shapefile
    with collection (DataDirectory+catchment_shapefile, 'r') as input:
        #schema = input.schema.copy()
        for f in input:
            #poly = Polygon(shape(f['geometry']))
            shapes.append(Polygon(shape(f['geometry'])))
            catchment_ids.append(f['properties']['OBJECTID'])
            #poly_x, poly_y = poly.exterior.xy
            #ax.plot(poly_x, poly_y, color='blue', linewidth=3)

    # read in the hydro points
    with collection (DataDirectory+points_shapefile, 'r') as input:
        points=[]
        point_ids=[]
        for p in input:
            # only append the sources
            if p['properties']['HYDRONODE_'] == 'source':
                #point_x = p['geometry']['coordinates'][0]
                #point_y = p['geometry']['coordinates'][1]
                points.append(Point(p['geometry']['coordinates'][0], p['geometry']['coordinates'][1]))
                point_ids.append(p['properties']['OBJECTID'])
                #ax.scatter(point_x, point_y, color='red')

    n_points = len(points)
    n_shapes = len(shapes)
    print "Number of sources: ", n_points
    print "Number of catchments: ", n_shapes

    # more efficient way of looping? This only loops through all the catchments once rather than having to do this multiple times.
    for i in range(n_shapes):
        catchment_id = catchment_ids[i]
        cols = [[] for i in range(3)]
        for j in range (n_points):
            if (shapes[i].contains(points[j])):
                cols[0].append(point_ids[j])
                cols[1].append(points[j].x)
                cols[2].append(points[j].y)

        if cols:
            this_csv_name = DataDirectory+'MM_sources_'+str(catchment_id)+'.csv'
            with open(this_csv_name, 'wb') as f:
                writer = csv.writer(f)
                writer.writerow(['OBJECTID', 'X', 'Y'])
                writer.writerows(zip(*cols))
            print "Done ID", catchment_id

    print "Done!"


if __name__ == '__main__':

    DataDirectory = '/home/s0923330/Datastore/5m_dems/scotland/Catchment_boundaries/sources_all_catchments/'
    catchment_shapefile = 'catchments_scotland.shp'
    points_shapefile = 'hydro_nodes_scotland.shp'
    extract_source_points(DataDirectory,catchment_shapefile,points_shapefile)
