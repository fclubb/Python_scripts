"""
Create a CSV file of source points from the OS MasterMap Water Network
Layer for each catchment in Scotland using  and shapely
FJC
23/01/17
"""

def extract_source_points(DataDirectory, catchment_shapefile, points_shapefile):

    from fiona import collection
    from shapely.geometry import shape, Point
    import csv

    # read in the catchment shapefile
    with collection (DataDirectory+catchment_shapefile, 'r') as input:
        schema = input.schema.copy()
        shapes = []
        catchment_ids = []
        for f in input:
            shapes.append(shape(f['geometry']))
            catchment_ids.append(f['properties']['OBJECTID'])

    # # read in the hydro points
    with collection (DataDirectory+points_shapefile, 'r') as input:
        points=[]
        for p in input:
            # only append the sources
            if p['properties']['HYDRONODE_'] == 'source':
                points.append(Point(p['geometry']['coordinates'][0], p['geometry']['coordinates'][1]))

    # for each polygon, check for points inside it
    for i in range(len(shapes)):
        this_csv_name = DataDirectory+'MM_sources_'+str(catchment_ids[i])+'.csv'
        coords = [[] for i in range(2)]
        for j in range(len(points)):
            if points[j].within(shapes[i]) == True:
                #push points back to csv
                x,y = points[j].xy
                coords[0].append(x)
                coords[1].append(y)
                print coords
        # now write these points to a csv file
        with open(this_csv_name, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(zip(*coords))


if __name__ == '__main__':

    DataDirectory = '/home/s0923330/Datastore/5m_dems/scotland/Catchment_boundaries/'
    catchment_shapefile = 'catchments_scotland.shp'
    points_shapefile = 'hydro_nodes_scotland.shp'
    extract_source_points(DataDirectory,catchment_shapefile,points_shapefile)
