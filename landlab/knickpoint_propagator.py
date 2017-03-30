################################################################################
#
#  knickpoint_propagator.py
#  A python script to create a model with landlab
#  and propagate knickpoints up through the
#  landscape
#  FJC 30/03/17
################################################################################

#import modules
import numpy as np
from pylab import show, figure, plot
import time
from landlab import RasterModelGrid
from landlab.components.flow_routing import FlowRouter
from landlab.plot.imshow import imshow_node_grid

# create a raster grid
mg = RasterModelGrid((50,50), 5., 5.)
# make a flat surface dipping down to the south
z = np.zeros(100, dtype=float)
z = mg.node_y*0.01
z+= np.random.rand(100.)/100000

# set the boundary conditions
mg.set_fixed_value_boundaries_at_grid_edges(False,True,False,True)
mg.set_closed_boundaries_at_grid_edges(True,False,True,False)



fr = FlowRouter(mg, './params.txt')
