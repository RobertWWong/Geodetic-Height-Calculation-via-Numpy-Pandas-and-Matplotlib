import numpy as np

'''
The purpose of this module is to create matrixes from files
It will use two different method of loading a file into a matrix

loadtxt and genfromtxt
'''

def loadfile(filename : str, skiprows = 0 ,  delimiter=None ):
    '''
    This function will return to a matrix after reading an input file
    This matrix object is addressable via matlab notation, but does not support
    attribute assignment.
    ie P.X = value
    '''
    return np.loadtxt(filename, skiprows=skiprows,    delimiter=delimiter)

def genload_file(fname :str,  delimiter=None, skip_header=0, skip_footer=0, names =True):
    '''
    ONLY USE THIS IF YOU HAVE A FILE WITH HEADER COLUMNS OTHERWISE THERE WILL BE NO EFFICENT ADDRESSING OF THE RETURN OBJECT\n

    This function will return a matrix that can access its column by name (label) \n\n
    It disallows addressing via matlab notation, but will allow standard 2D array addressing
    ie      matrix['Column_name'] == matrix[:,0]                     allowed
            (matrix[:,0] , matrix[:][0])  !=  matrix['Column_name']  disallowed
    '''
    return  np.genfromtxt(fname,  delimiter=delimiter, skip_header=skip_header, skip_footer=skip_footer, names=names)

def readbinary(fname, count=-1, sep=''):
    return np.fromfile(fname, dtype=float  ,count=count, sep=sep)

def variableLoad(fname, skiprows ):
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
        while n<leng:
            list_of_mat += a[start:end] #add into the list the data cluster during the intervals

            # Describes the starting index interval
            start = n+2

            #Update our index var to two rows before the next position row
            n += int(a[n+1][1])+1

            # Describes our ending index interval
            end= n +1
        print("We're done")
    except:
        pass
    narr = np.matrix(list_of_mat)
    # print(narr[-26:-1,0])
    return narr
    