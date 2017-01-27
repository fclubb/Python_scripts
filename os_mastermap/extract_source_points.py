"""
Create a CSV file of source points from the OS MasterMap Water Network
Layer for each catchment in Scotland using  and shapely
FJC
23/01/17
"""

def extract_source_points(DataDirectory, catchment_shapefile, points_shapefile):

    from fiona import collection
    from shapely.geometry import shape, Polygon, Point
    import csv
    from matplotlib import pyplot as plt
    from operator import itemgetter


    # plot for testing
    fig = plt.figure(1, figsize=(10,10))
    ax = fig.add_subplot(111)

    shapes = []
    catchment_ids = []
    # read in the catchment shapefile
    with collection (DataDirectory+catchment_shapefile, 'r') as input:
        #schema = input.schema.copy()
        for f in input:
            poly = Polygon(shape(f['geometry']))
            shapes.append(Polygon(shape(f['geometry'])))
            catchment_ids.append(f['properties']['OBJECTID'])
            poly_x, poly_y = poly.exterior.xy
            ax.plot(poly_x, poly_y, color='blue', linewidth=3)

    # read in the hydro points
    with collection (DataDirectory+points_shapefile, 'r') as input:
        points=[]
        point_ids=[]
        for p in input:
            # only append the sources
            if p['properties']['HYDRONODE_'] == 'source':
                point_x = p['geometry']['coordinates'][0][0]
                point_y = p['geometry']['coordinates'][0][1]
                points.append(Point(p['geometry']['coordinates'][0][0], p['geometry']['coordinates'][0][1]))
                point_ids.append(p['properties']['OBJECTID'])
                ax.scatter(point_x, point_y, color='red')

    # save figure for debug
    OutputFigureName = 'tay_check'
    OutputFigureFormat = 'pdf'
    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat, dpi=100)
    plt.close()

    n_points = len(points)
    n_shapes = len(shapes)
    print "Number of sources: ", n_points
    print "Number of catchments: ", n_shapes

    # for each polygon, check for points inside it
    catchment_points = []
    for i in range(n_points):
        for j in range(n_shapes):
            if points[i].within(shapes[j]) == True:
                # for each point push back the catchment ID that it is in
                catchment_points.append(catchment_ids[j])

    for catchment_id in catchment_ids:
        # write csv file for each catchment ID
        point_indices = [i for i, x in enumerate(catchment_points) if catchment_points[i] == catchment_id]
        these_points = itemgetter(*point_indices)(points)
        these_ids = itemgetter(*point_indices)(point_ids)
        cols = [[] for i in range(3)]
        for i in range(len(these_points)):
            cols[0].append(these_ids[i])
            cols[1].append(these_points[i].x)
            cols[2].append(these_points[i].y)

        this_csv_name = DataDirectory+'MM_sources_'+str(catchment_id)+'.csv'
        with open(this_csv_name, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(['OBJECTID', 'X', 'Y'])
            writer.writerows(zip(*cols))

if __name__ == '__main__':

    DataDirectory = '/home/s0923330/Datastore/5m_dems/scotland/Catchment_boundaries/sources_all_catchments/'
    #DataDirectory = 'Z:\\5m_dems\\scotland\\Catchment_boundaries\\'
    catchment_shapefile = 'catchments_scotland.shp'
    points_shapefile = 'hydro_nodes_scotland.shp'
    extract_source_points(DataDirectory,catchment_shapefile,points_shapefile)
