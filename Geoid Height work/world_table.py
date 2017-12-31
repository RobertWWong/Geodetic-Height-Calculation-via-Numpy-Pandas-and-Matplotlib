import numpy as np
import pandas as pd
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
    lat_or_long = 1 if islat_long else -1

    if lat_long>=0:
        div = int(-1*lat_long/10) if not islat_long else div

        if rem == 0:    # If our point is directly on the map, access the table directly.  y1=y2
            return base-div,base-div
        else:       # Our lat_long value lies between two other lat_long point
            return base-div, base-div-lat_or_long     # y1 and y2 are different
    else:
        div = int(-1*lat_long/10) if islat_long else div
        if rem ==0:
            return base+div,base+div
        else:
            return base+div, base+div+lat_or_long

def demo_boundary_search():
    test = [189, 180 ,182, 90, 50.23 , 50, 49.99, 0 ,-1, -9.9, -45, -59.9, -89, -91.2, -178, -179.21, -180, -181]

    for coord_val in test:
        print("test for latitude search:  ",coord_val)
        print(find_lat_or_long(coord_val))

        print("test for longitude search",coord_val)
        print(find_lat_or_long(coord_val,0), end='\n\n')

demo_boundary_search()

# nx = -113.4152
# ny = 43.536
def get_index(xlist, ylist):
    return [long_dict[i]for i in xlist] + [lat_dict[i] for i in ylist]

def get_degrees(xIndex, yIndex):
    return [ pworld.iloc[y1,x1]]


def find_four(nx, ny):
    print("Interpolating for || lat {} and long {}||".format(ny,nx))
    x1,x2 = find_lat_or_long(nx,0)  # Find longitudinal coordinates
    y1,y2 = find_lat_or_long(ny)    # Find latitudinal coordinates
    print('Here are our table index values\nx1: {}\ny1: {}\nx2: {}\ny2: {}\n'.format(x1,y1,x2,y2))

    Y1,Y2,X1,X2 = get_degrees([x1,x2], [y1,y2])
    print("Here is our table degree values for each point:\nX1: {}\nY1: {}\nX2: {}\nY2: {}\n".format(X1,Y1,X2,Y2))

    n11 = pworld.iloc[y1,x1]
    n12 = pworld.iloc[y2,x1]
    n21 = pworld.iloc[y1,x2]
    n22 = pworld.iloc[y2,x2]
    print("Here is table's geoid value (also, you miswrote a geoid value for nx2): ")
    print("n11: {}\nn12: {}\nn21: {}\nn22: {}\n".format(n11,n12,n21,n22))

    nx1= ((X2-nx) *n11 + (nx-X1)*n21 )/ (X2-X1)
    nx2= ((X2-nx) *n12 + (nx-X1)*n22 )/ (X2-X1) # it is n12 and n22,  word doc written asked for n12 and n11, which is incorrect
    nxy = ((Y2-ny)/(Y2-Y1))*nx1 +((ny-Y1)/(Y2-Y1))*nx2
    print("Our interpolated value from coordinates ({}, {}) is {}\nEnd of Program".format(nx,ny,nxy))

    return nxy


x1,x2 = find_lat_or_long(nx,0)  # Find longitudinal coordinates
y1,y2 = find_lat_or_long(ny)    # Find latitudinal coordinates

get_index([x1,x2],[y1,y2])

nx = 54.5
ny = 17.041667

find_four(nx,ny)

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
import scipy.interpolate as sc

sc.RectBivariateSpline(xmat, ymat, zmat)

pworld


dx, dy = 0.4, 0.4
xmax, ymax = 2, 4
x = np.arange(-xmax, xmax, dx)
y = np.arange(-ymax, ymax, dy)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(2*X)**2 - (Y/2)**2)

X.shape
Y.shape
Z.shape
interp_spline = sc.RectBivariateSpline(y, x, Z)

interp_spline.degrees
