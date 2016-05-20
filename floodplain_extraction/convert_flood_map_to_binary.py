#loads a shapefile of flood zones and adds a new field with a binary classification of the 
#flood zone.  No floodplain = 0; floodplain = 1.
#Fiona Clubb 16/05/16
#
import shapefile
#import os
#from osgeo import gdal

#Read in the shapefile
r = shapefile.Reader('Flood_zones_clip')

#Create a new shapefile in memory
w = shapefile.Writer()
w.fields = list(r.fields)

print len(r.records())

#Add a new field for the binary floodplain classification
w.field('BINARY', 'F', len(r.records()), 2)

# Loop through the existing shapefile
for rec in r.records():
    #print rec[4]
    if rec[4] == 'X':
        rec.append(0.0)
    else:
        rec.append(1.0)
    w.records.append(rec)

#Add modified record to the new shapefile
#w.records.append(rec)
print w.records

#Cope over the geometry
w._shapes.extend(r.shapes())

#Save as a new shapefile
new_shapefile = 'Flood_zones_clip_binary'
w.save(new_shapefile)

