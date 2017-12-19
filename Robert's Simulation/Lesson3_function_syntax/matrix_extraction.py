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
