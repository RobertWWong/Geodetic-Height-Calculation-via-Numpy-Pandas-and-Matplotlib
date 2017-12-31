# OBJECTIVES:Determing the indexes of lat_longitude
#    lat_longitude row vectors: X1(X1_index) and X2(X2_index)
#    Longitude column vectors: Y1(Y1_index) and Y2(Y2_index)
#
# lat_longitude test points within [-90 deg, +90 deg]
X = [89.9999,70.0,69.9999999,10.0,0.0,-10.0,-69.9999999,-70,-89.9999]# N/S lat_longitude

Xb=9#Xb=max(X)/10 for lat_longtitude Xb=9 and longitude Yb=18
Delta=10# ten-degrees intervals
for i in range (len(X)):
    TP=i+1
    print ('========== Test point lat_longitudes (deg) = ',TP)
    R=X[i]%10
    if X[i]>0:
        X1=int(X[i]-R)
        X1_index=int(Xb-(X1/Delta))
        if R==0:
            X2=X1
            X2_index=X1_index
        else:
            X2=X1+Delta
            X2_index=X1_index-1
    else:
        X1=int(X[i]-R)
        X1_index=int(Xb+abs(X1/Delta))
        if R==0:
            X2=X1
            X2_index=X1_index
        else:
            X2=X1+Delta
            X2_index=X1_index-1

    #print ('===============================')
    print('X=',X[i])
    print('X1=',X1)
    print('X2=',X2)
    print('X1_index=',X1_index)
    print('X2_index=',X2_index)
print ('===============================')
print ('End of the program for the lat_longitude-index determination')
# Longitude test points within [-180 deg, +180 deg]
Y = [-179.9999,-170.0,-169.9999999,-10.0,0.0,10.0,169.9999999,170,179.9999]# N/S lat_longitude
Yb=18#Yb=max(Y)/10 for lat_longtitude Yb=9 and longitude Yb=18
Delta=10# ten-degrees intervals
print ('Starting the longitude-index determination')
for i in range (len(Y)):
    TP=i+1
    print ('========== Test point longitude (deg) = ',TP)
    R=Y[i]%10
    if Y[i]<0:######
        Y1=int(Y[i]-R)
        Y1_index=int(Yb+(Y1/Delta))
        if R==0:
            Y2=Y1
            Y2_index=Y1_index
        else:
            Y2=Y1+Delta
            Y2_index=Y1_index+1
    else:
        Y1=int(Y[i]-R)
        Y1_index=int(Yb+abs(Y1/Delta))
        if R==0:
            Y2=Y1
            Y2_index=X1_index
        else:
            Y2=Y1+Delta
            Y2_index=Y1_index+1

    #print ('===============================')
    print('Y=',Y[i])
    print('Y1=',Y1)
    print('Y2=',Y2)
    print('Y1_index=',Y1_index)
    print('Y2_index=',Y2_index)
print ('===============================')
print ('End of the program for lthe ongitude index determination')


def find_four(nx, ny,world_table):
    print("Interpolating for || lat {} and long {}||".format(ny,nx))
    x1,x2 = find_lat_or_long(nx,0)  # Find longitudinal coordinates
    y1,y2 = find_lat_or_long(ny)    # Find latitudinal coordinates
    print('Here are our table index values\nx1: {}\ny1: {}\nx2: {}\ny2: {}\n'.format(x1,y1,x2,y2))

    Y1,Y2,X1,X2 = get_degrees([x1,x2], [y1,y2])
    print("Here is our table degree values for each point:\nX1: {}\nY1: {}\nX2: {}\nY2: {}\n".format(X1,Y1,X2,Y2))

    n11, n12, n21, n22 = get_geoid([X1,X2],[Y1,Y2],world_table)

    print("Here is table's geoid value (also, you miswrote a geoid value for nx2): ")
    print("n11: {}\nn12: {}\nn21: {}\nn22: {}\n".format(n11,n12,n21,n22))

    nx1= ((X2-nx) * n11 + (nx-X1) * n21 ) / (X2-X1)
    nx2= ((X2-nx) * n12 + (nx-X1) * n22 ) / (X2-X1) # it is n12 and n22,  word doc written asked for n12 and n11, which is incorrect
    nxy = ((Y2-ny)/(Y2-Y1))*nx1 +((ny-Y1)/(Y2-Y1))*nx2
    print("Our interpolated value from coordinates ({}, {}) is {}\nEnd of Program".format(nx,ny,nxy))

    return nxy

##
##
##X=69.9999999#X>0
##R=X%10
##
##x=X-R
##Xb=9
##X1=int(Xb-(x/10))
##if R==0:
##    X2=X1
##else:
##    X2=X1-1#X>0
##print ('X>0: X=',X)
##print ('R=',R)
##print ('x=',x)
##print ('X1=',X1)
##print ('X2=',X2)
##
##print ('=====================')
##
##X=-69.9999999#X<0
##Xb=9#Xb=max(X)/10
##X=abs(X)
##R=X%10
##x=X-R
###X1=int(Xb-(x/10))
##X1=int(Xb+(x/10))
##if R==0:
##    X2=X1
##else:
##    X2=X1+1#X>0
##print ('X<0: X=',X)
##print ('R=',R)
##print ('x=',x)
##print ('X1=',X1)
##print ('X2=',X2)
##print ('=====================')

print ('=====================')
