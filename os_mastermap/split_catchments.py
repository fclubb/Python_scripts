"""
Create individual shapefiles for each catchment in Scotland from the national
dataset - used to run each catchment separately
FJC
31/01/17
"""

# set backend to run on the server
import matplotlib
matplotlib.use('Agg')

import fiona
from shapely.geometry import shape, mapping

def split_polygons(DataDirectory, catchment_shapefile):

    with fiona.open(DataDirectory+catchment_shapefile) as input:
        for multi in input:
            catchment_id = multi['properties']['GI02_CATCH']
            this_output_name = 'catchment_'+str(catchment_id)+'.shp'
            with fiona.open(DataDirectory+this_output_name, 'w', driver=input.driver, crs=input.crs,schema=input.schema) as output:
                output.write({'properties': multi['properties'], 'geometry': mapping(shape(multi['geometry']))})


if __name__ == '__main__':

    DataDirectory = '/home/s0923330/Datastore/5m_dems/scotland/Catchment_boundaries/all_catchments/'
    catchment_shapefile = 'catchments_scotland.shp'
    split_polygons(DataDirectory,catchment_shapefile)
