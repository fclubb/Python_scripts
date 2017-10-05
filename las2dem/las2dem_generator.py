#---------------------------------------------------------------------#
# This script generates a series of bash scripts that can be used to
# transform a series of .las files into DTMs.
# Firstly, I use PDAL to classify the las files and filter so we only
# have ground returns, based on a PDAL tutorial:
# https://www.pdal.io/tutorial/pcl_ground.html
# Then I use points2grid to grid the ground returns into a DTM:
# https://github.com/CRREL/points2grid
# Finally, some good old gdal to translate to ENVI bil and fill no data
# holes in the raster.
#
# FJC (stolen and modified from a script that Stuart wrote)
# 04/10/17
#---------------------------------------------------------------------#

def p2gScripter(DataDirectory, Cores, UTMZone, Resolution, Hillshade=False):
    '''
    Generate the bash files for filtering, gridding, and translating.

    Args:
        DataDirectory (str): the directory to look for the las files
        Cores (int): number of cores you want to run it on (=n bash scripts)
        UTMZone (str): the UTM zone that you want to convert the data to
        Resolution (str): the grid resolution you want
        Hillshade (bool): if true, hillshade the DEMs. default = false

    Returns: 3 bash scripts which can be run in sequence to filter, grid,
    and prepare your data.

    Author: FJC

    '''

    import math
    from glob import glob
    import os, os.path

    # get total number of files
    n_files =  len([name for name in os.listdir(DataDirectory) if '.las' in name])
    print n_files

    for n in range(Cores):

        with open('pdal_Script' + str(n)+'.sh', 'w') as pdal, \
                open('p2g_Script' + str(n)+'.sh', 'w') as p2g, \
                    open('gdal_Script' + str(n)+'.sh', 'w') as gdal:
            print '\n Writing to pdal_Script' + str(n)+'.sh'
            print '\n Writing to p2g_Script' + str(n)+'.sh'
            print '\n Writing to gdal_Script' + str(n)+'.sh'

            # write the shebangs for the scripts\
            pdal.write('#!/bin/bash\n')
            p2g.write('#!/bin/bash\n')
            gdal.write('#!/bin/bash\n')

            # get each las file in the directory
            for FileName in glob(DataDirectory+"*.las")[n::Cores]:

                print "filename is: " + FileName

                # get the name of the LAS file
                split_fname = FileName.split('/')
                split_fname = split_fname[-1]

                # remove LAS extension from filename
                fname_noext = split_fname.split('.')
                fname_noext = fname_noext[0]

                pdal_str = ('pdal pcl -i %s -o %s -p classify.json' % (split_fname, fname_noext+'_ground.las'))

                SearchRadius = str(int(math.ceil(float(Resolution) * math.sqrt(2))))
                Resolution = str(Resolution)

                p2g_str = ('points2grid -i %s -o %s --idw --fill_window_size=7 '
                           '--output_format=arc --resolution=%s -r %s'
                           % (fname_noext+'_ground.las', fname_noext, Resolution, SearchRadius))

                gdal_str = ("gdalwarp -t_srs \'+proj=utm +zone=%s "
                            "+datum=WGS84\' -r cubic -of ENVI -dstnodata -9999 -ot Float32 %s.idw.asc %s_DEM.bil"
                            % (UTMZone, fname_noext, fname_noext))

                fill_str = ("gdal_fillnodata.py -md 20 -si 1 %s_DEM.bil" % (fname_noext))

                del_str = ('rm %s.idw.asc\n' % fname_noext)

                # write the commands to the 2 scripts
                pdal.write('nice ' + pdal_str + '\n')
                p2g.write('nice ' + p2g_str + '\n')
                gdal.write('nice ' + gdal_str + '\n')
                gdal.write('nice ' + fill_str + '\n')
                gdal.write(del_str)
                if Hillshade:
                    hs_str = ('gdaldem hillshade -of ENVI '
                              '%s_DEM.bil %s_HS.bil\n'
                              % (fname_noext, fname_noext))
                    gdal.write(hs_str)

    print '\tScripts successfully written.'

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5 and len(sys.argv) != 6:
        sys.exit('\nIncorrect number of arguments.\n\nPlease enter a data'
                 'directory, a UTM zone number, the grid resolution, and'
                 'set the hillshade flag (optional). Run with: '
                 'las2dem_generator.py /path/to/folder/ 10 2 True\n')

    if (len(sys.argv) == 6):
        p2gScripter(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], int(sys.argv[5]))
    if (len(sys.argv) == 5):
        p2gScripter(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
