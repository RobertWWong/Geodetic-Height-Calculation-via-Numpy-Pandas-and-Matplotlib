# OBJECTIVES:Determing the indexes of latitude
#    Latitude row vectors: X1(X1_index) and X2(X2_index)
#    Longitude column vectors: Y1(Y1_index) and Y2(Y2_index)
#
# Latitude test points within [-90 deg, +90 deg]
X = [89.9999,70.0,69.9999999,10.0,0.0,-10.0,-69.9999999,-70,-89.9999]# N/S latitude

Xb=9#Xb=max(X)/10 for lattitude Xb=9 and longitude Yb=18
Delta=10# ten-degrees intervals
for i in range (len(X)):
    TP=i+1
    print ('========== Test point latitudes (deg) = ',TP)    
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
print ('End of the program for the latitude-index determination')
# Longitude test points within [-180 deg, +180 deg]
Y = [-179.9999,-170.0,-169.9999999,-10.0,0.0,10.0,169.9999999,170,179.9999]# N/S latitude
Yb=18#Yb=max(Y)/10 for lattitude Yb=9 and longitude Yb=18
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
