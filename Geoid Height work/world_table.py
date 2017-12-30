import numpy as np
import pandas as pd
print('hello world')

world = np.loadtxt('world.csv', dtype = int, delimiter =',')
mworld = np.matrix(world)

pworld = pd.read_csv('world.csv',delimiter=',', header =None )
pworld[36] = pworld[0]

# This is to add another column to our array
wrap_world = np.hstack([world, world[:,0:1]])

o =np.array([[1,2,3],[12,12,12], [2,2,2]])
np.hstack(( o ,o[0:1].T) )
tr = np.empty((19,37,2))
# Another way to make a 3d array
tr[:,:,0] = pworld
tr[:,1,0]
tr[18,1,0]


def dms_to_degrees(degree_min_sec : list):
    '''
    This function will convert a degree : min : sec notated format to the standard degree format
    1 degree = 60 minutes     |    1 minute = 60 seconds
    1 minute = 1/60 D         |    1 second = 1/3600 D
    '''
    deg = degree_min_sec[0];        minutes = degree_min_sec[1];        sec = degree_min_sec[2]
    return sum([deg,minutes,sec])
x = 15
10 < x<20

def find_four_coord(lat_long ):
    '''
    Given some point on the map, we will find four adjacent coordinates that will be used
    to interpolate our given lat_long.

    The interpolated values should be our geoid height.
    Our world table already contains the geoid heigh given a lat and long by a 10 degrees increments.

    '''
