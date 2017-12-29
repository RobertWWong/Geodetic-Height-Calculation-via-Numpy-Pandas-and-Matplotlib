import numpy as np
import struct as s

# This is the available formatting given a GEPH file.
dRtype = np.dtype("f8,i2,i2,(1,3)i4,(1,10)f4,(1,8)f8")
dLtype = np.dtype("<f8,<i2,<i2,(1,3)<i4,(1,10)<f4,(1,8)<f8")
dBtype = np.dtype(">f8,>i2,>i2,(1,3)>i4,(1,10)>f4,(1,8)>f8")
oneByone = np.dtype("f8,i2,i2,i4,i4,i4,i4,i4,i4,i4,i4,i4,f4,f4,f4,f4,f8,f8,f8,f8,f8,f8,f8,f8")


def read_header_data(fname:str, traditional_reading = False):
    '''
    This requires a MRFIL.ASC file to work properly

    This function will load to a matrix a file with a
    structured yet variable amount of columns
    '''

    with open(file=fname , mode ='r') as f:
        allD = [x.split() for x in f.readlines()]
    a =allD
    # print(a[0:5])
    del a[0:5]      # Delete the first 5 lines

    # Load the asc file and iteratively select row values into matrix form
    print("Begin itereation\n\n")
    list_of_mat = []
    n = int(a[0][1])
    leng = len(a)

    print(n,leng)
    start=1
    end = n+1
    try:
        while end < leng:
            list_of_mat += a[start:end] #add into the list the data cluster during the intervals

            # Describes the starting index interval
            start = n+2

            #Update our index var to two rows before the next position row
            n += int(a[n+1][1])+1

            # Describes our ending index interval
            end= n +1
        print("We're done")
    except Exception as e:
        print("Error in variable load: ", e)
        print("n:{}  vs start:{} vs end:{}".format(n,start,end))
        pass
    narr = np.matrix(list_of_mat)
    # print(narr[-26:-1,0])
    return narr
