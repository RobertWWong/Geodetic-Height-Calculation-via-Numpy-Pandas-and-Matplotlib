import numpy as np
import pandas as pd
import scipy.interpolate as sc

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



print('hello world')
print("Consider these sites for interpolat_longion ")

print("https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.interp.html")
print('https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.interpolat_longe.interp2d.html')
print('https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.interpolat_longe.RectBivariateSpline.html')

# Global index searcher for fast and efficient look up with constant space complexity
lat_dict = { i: 90-10*i if i<10 else -(10*i -90) for i in range(19)}
long_dict = {i: -180+10*i if i<18 else (10*i-180) for i in range(37)}

# Two different ways to generate a map
# Matrix is necessary for mat plot lib 3d creation
world = np.loadtxt('world.csv', dtype = int, delimiter =',')
wrap_world = np.hstack([world, world[:,0:1]])
mworld = np.matrix(world)

# This is the panda matrix we will be using to display our data.
pworld = pd.read_csv('world.csv',delimiter=',', names =list(long_dict.values()))
pworld.index = lat_dict.values()    # change our row index name to their respective latitudinal values


#
#
# def dms_to_degrees(degree_min_sec : list):
#     '''
#     This function will convert a degree : min : sec notated format to the standard degree format
#     1 degree = 60 minutes     |    1 minute = 60 seconds
#     1 minute = 1/60 D         |    1 second = 1/3600 D
#     '''
#     deg = degree_min_sec[0];        minutes = degree_min_sec[1];        sec = degree_min_sec[2]
#     return sum([deg,minutes,sec])

def find_four_coord(lat_long_long ):

    return


def find_lat_or_long(lat_long , islat_long =True):
    '''
    Y1 <= Y <= Y2       or X1 <= X <= X2
    Given a lat value between (N 90) and (S -90), return y1 and y2 boundary values that it falls between.
    OR
    Given a long between(W -180) and (E 180), return x1 and x2 boundary values that it falls between.
    islat_long is default to check for latitude.

    rtype: (y1, y2) or (x1,x2)      lat or long coordinates
    '''
    if (islat_long and abs(lat_long)>90) or (not islat_long and abs(lat_long) >180):
        print('Your lat_long values are out of bounds for your current search query: {} for {} '.format( lat_long, 'latitude' if islat_long else 'longitude'))
        return
    base = 9 if islat_long else 18
    rem = abs(lat_long)%10;             div = int(lat_long/10)      #Remainder and division elements for logical check

    # Latitude decrement to get y2 and longitude increment to get x2 for all positive values
    # Latitude and longitude will swap relationship  for all negative values
    lat_or_long = 1 if islat_long else -1

    # For any positive number
    if lat_long>=0:
        div = int(-1*lat_long/10) if not islat_long else div    # If we are checking for longitudinal bounds, make div value negative for a positive subtraction

        if rem == 0:    # If our point is directly on the map, access the table directly.  y1=y2
            return base-div,base-div
        else:       # Our lat_long value lies between two other lat_long point
            return base-div, base-div-lat_or_long     # The indexes are in increating order if searching for longitude, else decreasing for latitude
    else:
        div = int(-1*lat_long/10) if islat_long else div    # If we are checking for latitudinal bounds, make div val positive for negative addition
        if rem ==0:
            return base+div,base+div
        else:       # Our largest x value is the highest index, and vice versa for the y values. So switch the return order
            return base+div+lat_or_long, base+div   # Must reverse index position to maintain order

def demo_boundary_search():
    '''
    This function demos whether our values gathered fall into their respective lat/long boundaries,
    as well as returning a proper index
    '''
    test = [30.123456, -175.123456, -30.123456, 175.123456, 30, -140]

    for coord_val in test:
        print("test for latitude search:  ",coord_val)
        print(find_lat_or_long(coord_val))

        print("test for longitude search",coord_val)
        print(find_lat_or_long(coord_val,0), end='\n\n')

# demo_boundary_search()

def get_degrees(xlist, ylist):
    '''
    This function will return the degree values from a list of indexes,
    with ordering  X1,X2,Y1,Y2  where the first element of each axis is less than the second element.
    We will use our global variables long_dict and lat_dict to search degree val given an index key
    '''

    # This is called list comprehension, combined with list concatenation.
    return [long_dict[i]for i in xlist] + [lat_dict[i] for i in ylist]

def get_geoid(xIndex, yIndex,pworld):
    '''
    Given a row and column index list of two elements each with a panda table,
    return the 4 geoid height associated to those coordinates
    ie. n11,n12, n21, n22
    '''
    nlist = []
    for x in xIndex:
        for y in yIndex:
            nlist.append(pworld.iloc[y,x])
    return nlist

def interpX_Yd(Xlist_Ylist,Geoid_List, nyx_val):
    '''
    Perform a bilinear interpolations given four coordinates (list of xlist and ylist),
    along with their respective Geoid value (list)
    and the arbitrary X and Y value (list)
    '''
    X1,X2 = Xlist_Ylist[0]
    Y1,Y2 = Xlist_Ylist[1]

    n11, n12, n21, n22 = Geoid_List
    ny,nx = nyx_val

    nx1= ((X2-nx) *n11 + (nx-X1)*n21 )/ (X2-X1)
    nx2= ((X2-nx) *n12 + (nx-X1)*n22 )/ (X2-X1)
    nxy = ((Y2-ny)/(Y2-Y1))*nx1 +((ny-Y1)/(Y2-Y1))*nx2
    return nxy

def display_coords(latList, longLists, table_loc):
    '''
    This function will display a 4x4 ,2x1, or 1x2 geoid height table for a given coordinate list. It's a utility function.
    The values of each lists must be in increments of 10
    Element in lists are ordered from least to greatest
    '''
    lat1,lat2 = latList
    long1,long2 = longLists

    if lat1<lat2:
        lat1,lat2 = lat2, lat1

    if long1>long2:
        long1,long2 = long2, long1

    print('#'*15,'\n',table_loc.loc[lat1:lat2, long1:long2],'\n','#'*15)

def interp1D(X_Ydegrees, n11_n12, ny_x_val):
    '''
    Given that two of the coords fall in the same axis, only do interpolation in one direction.
    '''
    x_y1, x_y2 = X_Ydegrees
    n11,n12 = n11_n12
    Nxy = ((x_y2 - ny_x_val)/(x_y2-x_y1))*n11  +  ((ny_x_val - x_y1)/(x_y2 - x_y1)) * n12
    return Nxy

def find_four(nx, ny, pworld):
    '''
    Given some point on the map, we will find four adjacent coordinates that will be used
    to interpolat_longe our given lat_long_long.

    The interpolated values should be our estimated geoid height.
    Our world table already contains the geoid height given a lat_long and long by a 10 degrees increments
    '''

    print("Interpolating for || long {} and lat  {} ||".format(nx,ny))
    x1,x2 = find_lat_or_long(nx,0)  # Find longitudinal coordinates
    y1,y2 = find_lat_or_long(ny)    # Find latitudinal coordinates
    print('Here are our table index values\nx1: {}\ny1: {}\nx2: {}\ny2: {}\n'.format(x1,y1,x2,y2))

    X1,X2,Y1,Y2 = get_degrees([x1,x2], [y1,y2]  )
    print("Here is our table degree values for each point:\nX1: {}\nY1: {}\nX2: {}\nY2: {}\n".format(X1,Y1,X2,Y2))

    # Check for our edge corner case our xy coord being an index on the table
    if X1==X2 and Y1==Y2:
        print("Here's our geoid table\n")
        display_coords([Y1,Y2],[X1,X2], pworld)
        return pworld.loc[Y1,X1]

    geoid_list = n11, n12, n21, n22 = get_geoid([x1,x2],[y1,y2], pworld)

    print("Here is table's geoid value (also, you miswrote a geoid value for nx2): ")
    print("n12: {}\t\tn22: {}\nn11: {}\t\tn21: {}\n".format(n12,n22, n11,n21))

    # Logical check for our edge cases
    if Y1 == Y2:                  # Do interpolation on the X axis because Latitude is the same value
        print("Do interp in x axis")
        Xdeg_list = [X1,X2]
        x_geoid_val = n11,n21
        nxy = interp1D(Xdeg_list, x_geoid_val, nx)
    elif X1 == X2:             # Do interpolation on the Y axis because longitude is the same value
        print("Do interp in y axis")
        Ydeg_list = [Y1,Y2]
        y_geoid_val = n21,n22
        nxy = interp1D(Ydeg_list, y_geoid_val, ny)
    else:                         # All coord values are not on their respective axes
        nxy = interpX_Yd([[X1,X2],[Y1,Y2]],geoid_list, [ny , nx])


    print("Here's our geoid table\n")
    display_coords([Y1,Y2],[X1,X2], pworld)

    print("Our interpolated value from coordinates ({}, {}) is {}\nEnd of Program\n".format(ny,nx,nxy))

    return nxy


def demo_interp_cases():
    '''
    Demonstrate the interp conditions we met
    '''

    ny = 30.123456; nx = 175.123456
    input("Press enter to continue testing your cases 1: lat= {}   long = {}".format(ny,nx))
    find_four(nx,ny,pworld)

    input("Press enter to continue testing your cases 1: lat= {}   long = {}".format(ny,nx))
    ny = 30.123456; nx = -175.123456
    find_four(nx,ny,pworld)

    input("Press enter to continue testing your cases 1: lat= {}   long = {}".format(ny,nx))
    ny = -30.123456; nx = 175.123456
    find_four(nx,ny,pworld)

    input("Press enter to continue testing your cases 1: lat= {}   long = {}".format(ny,nx))
    ny = -30.123456; nx = -175.123456
    find_four(nx,ny,pworld)

    print('Time for case 2 and 3\n\n')

    input("Press enter to continue testing your cases 2: lat= {}   long = {}".format(ny,nx))
    ny = 30 ; nx = 175.123456
    find_four(nx,ny,pworld)

    input("Press enter to continue testing your cases 3: lat= {}   long = {}".format(ny,nx))
    ny = -30.123456; nx = -175
    find_four(nx,ny,pworld)

    print('Time for case 4\n\n')
    ny = -30; nx = -170
    input("Press enter to continue testing your cases 4: lat= {}   long = {}".format(ny,nx))
    find_four(nx,ny,pworld)



def do_plotting(mworld):
    '''
    This function will create a 3d mesh of the world, given the world matrix
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    row = np.array(list(lat_dict.values()))
    col = np.array(list(long_dict.values()))

    xrow,ycol = np.meshgrid(col,row)
    print("shape of our mesh is ",xrow.shape)

    fig = plt.figure(1)
    print('# Plotting Long vs Lat')
    ax = fig.add_subplot(111, projection = '3d')
    ax.set_title('Longitude x Latitude x Geoid Height')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Elevation')
    ax.plot_wireframe(xrow, ycol, mworld)

    print('# Plotting Lat vs Long')
    fig1 = plt.figure(2)
    ax1 = fig1.add_subplot(111, projection = '3d')
    ax.set_title('Latitude x Longitude x Geoid Height')
    ax1.set_xlabel('Latitude')
    ax1.set_ylabel('Longitude')
    ax1.set_zlabel('Elevation')

    ax1.plot_wireframe(ycol,xrow, mworld)

    plt.show()
