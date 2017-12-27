import numpy as np
import matrix_extraction as me
import struct as s

def data_splitter(geph_data, bytes_per_var :list=None):
    '''
    Takes a string object that is converted from a byte buffer and separate them into
    a more neatly spaced structure to read from.
    '''

    if bytes_per_var == None:
        geph_amt_per_record = [1,1,1,3,10,8]
    else:
        geph_amt_per_record = bytes_per_var


    start = 0
    my_list = []
    for i in geph_amt_per_record:
        my_list.append(geph_data[start:start+i])
        start = start+i
    return my_list

def read_header_data(fname:str,byte_per_low :int , data_type : int , traditional_reading = False):
        """
        This function will read to a list the first 80 bytes as its header
        It will continue reading the rest of the file in 128 bytes interval, until it reaches an EOF, into an ndarray
        The return type will be a tuple, containing the header byte value and the ndarray
        """

        # This is the available formatting given a GEPH file.
        dRtype = np.dtype("f8,i2,i2,(1,3)i4,(1,10)f4,(1,8)f8")
        dLtype = np.dtype("<f8,<i2,<i2,(1,3)<i4,(1,10)<f4,(1,8)<f8")
        dBtype = np.dtype(">f8,>i2,>i2,(1,3)>i4,(1,10)>f4,(1,8)>f8")
        oneByone = np.dtype("f8,i2,i2,i4,i4,i4,i4,i4,i4,i4,i4,i4,f4,f4,f4,f4,f8,f8,f8,f8,f8,f8,f8,f8")


        # This is for the gmes file input, of which the header follows, then a leader record describing the data record,
        # Then the actual data record of the binary files


        # Using a dictionary as a switch statement for the byte to value format
        data_switch = {1:dRtype,  2:dLtype , 3:dBtype , 4:oneByone }
        dtype = data_switch[data_type]

        with open(fname, mode ='rb') as fd:
            header = fd.read(80)

            # This statement will create our ndarray
            npArr = np.fromfile(fd, dtype =dtype)
            if not traditional_reading:
                return header, npArr

            #  The statement below will read 128 bytes into a numpy array until an eof is reached
            i = 0
            fd.seek(80)
            while fd.readable() and i<100:
                try:
                    buffer_list.append(fd.read(byte_per_low))
                    if buffer_list[i] == b'':
                        print("Breaking at {} rows\n".format(i))
                        buffer_list.pop()
                        return header,conversion_list

                    conversion_list.append(np.frombuffer(buffer_list[i],dtype=dtype))
                except Exception as e:
                    raise e
                i += 1

def read_bin_struct(fname: str):
    '''
    Specifically reading the geph files
    Here is another way to read a binary file into a specific format given its data structure
    '''
    with open(fname, mode ='rb') as fd:
    	header = fd.read(80)
    	data_rows = []
    	while fd.readable:
    		geph_data = s.unpack('=dhh3l10f8d', fd.read(128))
    		data_rows.append(geph_data)
    return header,data_rows

def write_np_txt(fout_name: str, ndarray : np.ndarray):
    '''
    Given a numpy array that IS NOT A VOID STRUCT
    (which occurs because of our formatting structure is nested --see dRtype in first function)
    write to a text file the content of the ndarray
    '''
    # Our formatting for each row
    fmt_dict = {'1':'f', '2':'d', '3':'d', '10':'e', '8':'e'}
    def all_split(fmt:str):    #Wrapper function to split the numpers correctly
        for amt,typ in fmt_dict.items():
            for i in range(int(amt)):
                padding =6
                if typ =='e':
                    padding = 15
                fmt += "%{pad}{typ}".format(typ = typ, pad=padding)
        return fmt
    fmt = all_split("")
    np.savetxt(fout_name, ndarray, fmt=fmt)
    print('Saving numpy file is complete!')
