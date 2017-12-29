import numpy as np

dRtype = np.dtype("f8,i2,i2,(1,3)i4,(1,10)f4,(1,8)f8")
oneByone = np.dtype("f8,i2,i2,i4,i4,i4,f4,f4,f4,f4,f4,f4,f4,f4,f4,f4,f8,f8,f8,f8,f8,f8,f8,f8")

def read_geph_data_frame(fname, dtype = dRtype ):
    '''
    Read a geph file into a numpy matrix
    '''
    with open(fname, mode ='rb') as fd:
        header = fd.read(80)
        npArr = np.fromfile(fd, dtype =dtype)
    return header, npArr


def turn_to_one(nparr):
    # Our function will turn the numpy data array into a more file friendly readble version
    nparr = list(nparr)
    return np.asarray(nparr,dtype = oneByone)

def save_to_text ( fname, nparr):
    """
    Function to save a nicely translated numpy array to a text document
    We will first turn our array into something nicer
    """
    nparr = turn_to_one(nparr)
    fmt= all_split('')
    np.savetxt(fname, nparr, fmt=fmt, delimiter=' ', newline='\n')


def all_split(fmt:str):
    '''
    Wrapper function to split the numpy array into a somewhat friend format
    '''
    fmt_dict = {'1':'f', '2':'d', '3':'d', '10':'e', '8':'e'}
    for amt,typ in fmt_dict.items():
        for i in range(int(amt)):
            padding =8
            if typ =='e':
                padding = 15
            fmt += "%{pad}{typ}".format(typ = typ, pad=padding)
    return fmt
