import numpy as np
import struct as s

# This is the available formatting given a GEPH file.
dRtype = np.dtype("f8,i2,i2,(1,3)i4,(1,10)f4,(1,8)f8")
dLtype = np.dtype("<f8,<i2,<i2,(1,3)<i4,(1,10)<f4,(1,8)<f8")
dBtype = np.dtype(">f8,>i2,>i2,(1,3)>i4,(1,10)>f4,(1,8)>f8")
oneByone = np.dtype("f8,i2,i2,i4,i4,i4,i4,i4,i4,i4,i4,i4,f4,f4,f4,f4,f8,f8,f8,f8,f8,f8,f8,f8")


def read_header_data(fname:str):
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
    n = int(a[0][1])        # This is the amount of rows for this current MRFIL frame
    leng = len(a)

    print(n,leng)
    start=1
    end = n+1
    try:
        while end < leng:
            list_of_mat += a[start:end] # add into the list the data cluster during the intervals
            start = n+2                 # Describes the starting index interval
            n += int(a[n+1][1])+1       # Update our index var to two rows before the next position row
            end= n +1                   # Describes our ending index interval
        print("We're done")
    except Exception as e:
        print("Error in variable load: ", e)
        print("n:{}  vs start:{} vs end:{}".format(n,start,end))
        pass

    # We have to convert our strings to their respective data types
    convert_string_to_val(list_of_mat)
    # Change it to a numpy matrix, accessing elements is a lot easier.
    nmat = np.matrix(list_of_mat)

    return nmat, list_of_mat


def convert_string_to_val(str_list):
    tmges,gps,parameters = float,int,float
    for row in range(len(str_list)):
        # These processes will convert our string to their respective types
        first = [tmges(str_list[row][0])]
        second = [gps(i) for i in str_list[row][1:5]]
        third = [parameters(i) for i in str_list[row][5:10]]
        str_list[row] = first+second+third  # This will modify our array by reference

def save_txt (fout, nMatrix):
    save_fmt = '%.6f' +'%8d'*4 + '%19.9e'*5
    np.savetxt(fout, nMatrix, fmt=save_fmt, delimiter=' ', newline='\n', header='', footer='', comments='# ')
