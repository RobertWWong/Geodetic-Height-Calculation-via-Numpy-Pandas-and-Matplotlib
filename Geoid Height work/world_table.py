import numpy as np
import pandas as pd
import scipy.interpolate as sc


print('hello world')
print("Consider these sites for interpolat_longion ")

print("https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.interp.html")
print('https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.interpolat_longe.interp2d.html')
print('https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.interpolat_longe.RectBivariateSpline.html')

# Global index searcher for fast and efficient look up with constant space complexity
lat_dict = { i: 90-10*i if i<10 else -(10*i -90) for i in range(19)}
long_dict = {i: -180+10*i if i<18 else (10*i-180) for i in range(37)}

# Two different ways to generate a map
world = np.loadtxt('world.csv', dtype = int, delimiter =',')
wrap_world = np.hstack([world, world[:,0:1]])
mworld = np.matrix(world)


pworld = pd.read_csv('world.csv',delimiter=',', names =list(long_dict.values()))
pworld.index = lat_dict.values()

# pworld.rename(index = lat_dict)     # or this
# This is to add another column to our array
# o =np.array([[1,2,3],[12,12,12], [2,2,2]])
# np.hstack(( o ,o[0:1].T) )
# tr = np.empty((19,37,2))
# Another way to make a 3d array
# tr[:,:,0] = pworld
# tr[:,1,0]
# tr[18,1,0]
pworld




def dms_to_degrees(degree_min_sec : list):
    '''
    This function will convert a degree : min : sec notated format to the standard degree format
    1 degree = 60 minutes     |    1 minute = 60 seconds
    1 minute = 1/60 D         |    1 second = 1/3600 D
    '''
    deg = degree_min_sec[0];        minutes = degree_min_sec[1];        sec = degree_min_sec[2]
    return sum([deg,minutes,sec])

def find_four_coord(lat_long_long ):
    '''
    Given some point on the map, we will find four adjacent coordinates that will be used
    to interpolat_longe our given lat_long_long.

    The interpolat_longed values should be our geoid height.
    Our world table already contains the geoid heigh given a lat_long and long by a 10 degrees increments
    '''
    return


def find_lat_or_long(lat_long , islat_long =True):
    '''
    Y1 <= Y <= Y2       or X1 <= X <= X2
    Given a lat value between (N 90) and (S -90), return y1 and y2 boundary values that it falls between.
    OR
    Given a long between(W -180) and (E 180), return x1 and x2 boundary values that it falls between.
    rtype: (y1, y2) or (x1,x2)      lat or long coordinates
    '''
    if (islat_long and abs(lat_long)>90) or (not islat_long and abs(lat_long) >180):
        print('Your lat_long values are out of bounds for your current search query: {} for {} '.format( lat_long, 'latitude' if islat_long else 'longitude'))
        return
    base = 9 if islat_long else 18
    rem = abs(lat_long)%10;             div = int(lat_long/10)

    # Latitude decrement to get y2 and longitude increment to get x2 for all positive values
    # Latitude and longitude will swap relationship  for all negative values
    lat_or_long = 1 if islat_long else -1

    if lat_long>=0:
        div = int(-1*lat_long/10) if not islat_long else div

        if rem == 0:    # If our point is directly on the map, access the table directly.  y1=y2
            return base-div,base-div
        else:       # Our lat_long value lies between two other lat_long point
            return base-div, base-div-lat_or_long     # y1 < y2 are different
    else:
        div = int(-1*lat_long/10) if islat_long else div
        if rem ==0:
            return base+div,base+div
        else:       # Our largest x value is the highest index, and vice versa for the y values. So switch the return order
            return base+div+lat_or_long, base+div

def demo_boundary_search():
    test = [189, 180 ,182, 90, 50.23 , 50, 49.99, 0 ,-1, -9.9, -45, -59.9, -89, -91.2, -178, -179.21, -180, -181]

    for coord_val in test:
        print("test for latitude search:  ",coord_val)
        print(find_lat_or_long(coord_val))

        print("test for longitude search",coord_val)
        print(find_lat_or_long(coord_val,0), end='\n\n')

# demo_boundary_search()

def get_degrees(xlist, ylist):
    return [long_dict[i]for i in xlist] + [lat_dict[i] for i in ylist]

def get_geoid(xIndex, yIndex,pworld):
    nlist = []
    for x in xIndex:
        for y in yIndex:
            nlist.append(pworld.iloc[y,x])
    return nlist

def interpX_Yd(Xlist_Ylist,Geoid_List, nyx_val):
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
    x_y1,x_y2 = X_Ydegrees
    n11,n12 = n11_n12
    Nxy = (x_y2-ny_x_val)/(x_y2-x_y1)*n11  +  (ny_x_val - x_y2)/(x_y2 - x_y1) * n12
    return Nxy

def find_four(nx, ny, pworld):
    print("Interpolating for || long {} and lat  {}||".format(nx,ny))
    x1,x2 = find_lat_or_long(nx,0)  # Find longitudinal coordinates
    y1,y2 = find_lat_or_long(ny)    # Find latitudinal coordinates
    print('Here are our table index values\nx1: {}\ny1: {}\nx2: {}\ny2: {}\n'.format(x1,y1,x2,y2))

    X1,X2,Y1,Y2 = get_degrees([x1,x2], [y1,y2]  )
    print("Here is our table degree values for each point:\nX1: {}\nY1: {}\nX2: {}\nY2: {}\n".format(X1,Y1,X2,Y2))

    if X1==X2 and Y1==Y2:
        return pworld.loc[Y1,X1]

    geoid_list = n11, n12, n21, n22 = get_geoid([x1,x2],[y1,y2], pworld)

    print("Here is table's geoid value (also, you miswrote a geoid value for nx2): ")
    print("n12: {}\t\tn22: {}\nn11: {}\t\tn21: {}\n".format(n12,n22, n11,n21))

    if Y1 == Y2:                  # Do interpolation on the X axis because Latitude is the same value
        Xdeg_list = [X1,X2]
        x_geoid_val = n11,n21
        nxy = interp1D(Xdeg_list, x_geoid_val, nx)
    elif X1 == X2:             # Do interpolation on the Y axis because longitude is the same value
        Ydeg_list = [Y1,Y2]
        y_geoid_val = n21,n22
        nxy = interp1D(Ydeg_list, y_geoid_val, ny)
    else:                         # All coord values are not on their respective axes
        nxy = interpX_Yd([[X1,X2],[Y1,Y2]],geoid_list, [ny , nx])

    # nx1= ((X2-nx) *n11 + (nx-X1)*n21 )/ (X2-X1)
    # nx2= ((X2-nx) *n12 + (nx-X1)*n22 )/ (X2-X1)
    # nxy = ((Y2-ny)/(Y2-Y1))*nx1 +((ny-Y1)/(Y2-Y1))*nx2

    print("Here's our geoid table\n")
    display_coords([Y1,Y2],[X1,X2], pworld)

    print("Our interpolated value from coordinates ({}, {}) is {}\nEnd of Program".format(ny,nx,nxy))

    return nxy

ny = 30.123456; nx = 175.123456
find_four(nx,ny,pworld)

ny = 30.123456; nx = -175.123456
find_four(nx,ny,pworld)

ny = -30.123456; nx = 175.123456
find_four(nx,ny,pworld)

ny = -30.123456; nx = -175.123456
find_four(nx,ny,pworld)





# xl = [x1,x2 ]= find_lat_or_long(nx,0)  # Find longitudinal coordinates
# yl = [y1,y2] = find_lat_or_long(ny)    # Find latitudinal coordinates
#
#
# xl
# a1,a2 = xl
# yl
# the_grid = pworld.iloc[7:8+1, 23:24+1]
# the_grid

# xx = [x1,x2,x1,x2]
# yy = [y1,y1,y2,y2]

# Trying scipy interpolate module
# sc.RectBivariateSpline(xx, yy, the_grid)    # x must be strictly increasing?

# yas =sc.interp2d(yy,xx,the_grid)
# yas(0,0)
#
#
#
#
# xd1,xd2, yd1,yd2 = get_degrees([x1,x2],[y1,y2])
# xd1,xd2, yd1,yd2
#
#
# display_coords([yd1,yd2], [xd1,xd2] , pworld )
# pworld.loc[yd1:yd2,xd1:xd2]        # Ahh i can access it via degrees using pandas.dataframes.loc[]
# ]
#
#
#
# n11,n21,n12,n22 = get_geoid([x1,x2],[y1,y2],pworld)
# n11,n21,n12,n22
#
# x11 = pworld.iloc[y1,x1]
# x12 = pworld.iloc[y2,x1]
# x21 = pworld.iloc[y1,x2]
# x22 = pworld.iloc[y2,x2]
# pworld.iloc[6:10, 20:27]

#
# y1, y2
# x1 ,x2
#
# Y1,Y2, X1,X2
# pworld.iloc[y1,x1]
# nx
# ny
#
#
# nx1
# nx2
#
# nxy = ((Y2-ny)/(Y2-Y1))*nx1 +((ny-Y1)/(Y2-Y1))*nx2
# nxy
#
# xmat = [x2,x2,x1,x1]
# ymat = [y1,y2,y1,y2]
# zmat = pworld.iloc[y2:y1+1,x1:x2+1]
# zmat


# sc.RectBivariateSpline(xmat, ymat, zmat)
#
# pworld
#
#
# dx, dy = 0.4, 0.4
# xmax, ymax = 2, 4
# x = np.arange(-xmax, xmax, dx)
# y = np.arange(-ymax, ymax, dy)
# X, Y = np.meshgrid(x, y)
# Z = np.exp(-(2*X)**2 - (Y/2)**2)
#
# X.shape
# Y.shape
# Z.shape
