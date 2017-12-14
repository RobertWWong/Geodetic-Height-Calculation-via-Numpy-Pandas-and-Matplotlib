import numpy as np

# We will be using numpy to help us read and write files from asc.
# Headers will also be explained below
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html
# This link is now what we will use to understand how to format the decimal place to their proper resolution

'''
Lesson 1:
Read and writing to files
Loading columns into a numpy matrix
Formatting file input
Formatting header inputs
'''

def read_write_YSFIL_Mat(input_asc : str, use_header : bool = False):
    '''
    This function will read an asc file and write to an output labeled
    YSFIL_Mat.txt       OR       YSFIL_Mat_Label.txt
    depending on the use_header argument

    It will write to the file a matrix of N X 37
    The first column will be formatted to 1 decimal of resolution
    The rest of the column will be formatted to 6 decimals of resolution
    '''

    # First, load your asc file into a numpy
    # We will also remove the first three rows of the file before saving the file
    asc_matrix = np.loadtxt(input_asc, skiprows=3)
    # print(asc_matrix[0])

    # This list contains the labels for each of the columns past the first.
    #The for loop after it will be appending a '_f' to each label to denote that it is a filter
    header_fmt = ["Time","pE","pF","pG","vE","vF","vG","r","p","hdg","aE","aF","aG","sf_fd","sf_rt","sf_dn","rDot","pDot","hdgDot","SpE","SpF","SpG","SvE","SvF","SvG","Sr","Sp","Shdg","SaE","SaF","SaG","Ssf_fd","Ssf_rt","Ssf_dn","SrDot","SpDot","ShdgDot"]
    for index in range (1,37):
        if input_asc.upper() == 'YSMTHAF.ASC':
            header_fmt[index]+='_s'
        else:
            header_fmt[index]+='_f'

    #Checking to see if we have missed a variable out of 37, if not, then an error will be raised
    assert len(header_fmt)==37
    assert (len(set(header_fmt))) ==37

    # file_format is used to format the resolution of our numbers, taken from the array.
    # Each column (except for the first) will be precise to 6 decimal places.
    # The formatting of the first decimal is 9 spaces to the right,
    # The formatting for the other decimals is 15 spaces with respect to the first decimal
    file_format = "".join(["%9.1f"]+["%15.6e"]*(asc_matrix.shape[1]-1))
    # print(file_format)

    #Use the correct prefix depending on user input
    prefix = '_Mat.txt'
    if use_header:
        prefix = '_Mat_Label.txt'
    output_file = input_asc.replace('.ASC', prefix)

    # We should remember the format that our asc file was in, which is binary. Use wb to write to binary.
    # The python convention to opening a file is to use the keyword "with" and "as"
    # This allows the user to rename our file object variable
    # As well as automatically closing our file whenever it exits out of scope.
    with open(output_file, mode='wb') as ourfile:
        header_format =""
        if use_header:
            # Now we need to format the header section as well.
            # Formatting depends on the file_format symbols used and their respective spacing
            # In our case, 9 and 15 were used to justify our spacing in  file_format
            header_format = header_fmt[0].rjust(9)
            for i in header_fmt[1:]:
                header_format += i.rjust(15)
        # Numpy method 'savetxt' requires a file_name and a properly formatted array type as a required argument.
        np.savetxt(ourfile,asc_matrix, fmt =file_format, header=header_format , newline='\r\n', comments='')


# Run demo
f1 ='YSFIL.ASC'
f2 = 'YSMTHAF.ASC'
f3 = 'Ytest.ASC'
f4 = 'Ytest_Mat_Label.txt'
read_write_YSFIL_Mat(f1,True)

# To read from header form to matrix form
asc_matrix = np.genfromtxt(f3, dtype=float, names=True)
print(asc_matrix[0:5,0])
print(asc_matrix["Time"])
