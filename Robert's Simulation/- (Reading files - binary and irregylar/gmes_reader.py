import numpy as np
import struct as s

def leader_reader(file ,off_set =0, numpy_array : bool =True):
    '''
    This function will read from a file the leader record of a new frame
    for EVERY NSAT amount of data record rows that it is called upon.
    Every leader record is always 33 bytes long of the format  "ddhh8bb"

    We will be ignoring the first 4 char bytes after the header record, as they are usually binary

    Return a list of relevant data, the Nsat value, and the Nmes value
    '''
    if off_set != 0:
        file.read(off_set)
    if not numpy_array:
        lead_fmt = '=ddhh8bb'  # for struct binary conversions, disregard the sync, it is in its final value state
        lead_size = s.calcsize(lead_fmt)    # This is the amount of bytes read on every function call
        lead_data = s.unpack(lead_fmt,  file.read(lead_size))   # Conversion from bytes to data types

        # Gather necessary data
        data_list = list(lead_data[0:4])        # Transform our converted leader record into a list
        Nsat, Nmes = lead_data[2:4]             # Get our Nsat and Nmes data values
        data_list.append(lead_data[4:4+Nmes])   # Get the Nmes amount of measurement
        data_list.append(lead_data[-1])         # This is the Uiode item value, either a 0 or 1
        return data_list, Nsat, Nmes
    else:
        # Same as above but for the numpy format
        numpy_fmt = np.dtype([('bin','4S'),('tmes','f8'),('dtclk','f8'),('nsat','i2'),('nmes','i2'),('imes','8i1'),('uiode','i1')])
        numpy_header = np.fromstring(file.read(33), dtype=numpy_fmt)
        return numpy_header

def data_reader(bufferStream, nsat :int , nmes :int, off_set =0):
    '''
    This function will read Nsat amount of rows from a gmes file and put them into the appropriate format
    '''
    if off_set !=0:
        bufferStream.seek(bufferStream.tell() + off_set)

    read_size = 14+nmes*8
    dtype = np.dtype('4i1, 2i4, {}f8,i2'.format(nmes))
    ndarr = np.fromstring(bufferStream.read(read_size), dtype=dtype)

    for i in range(nsat-1):
        next_row = np.fromstring(bufferStream.read(read_size), dtype=dtype)
        ndarr = np.vstack((ndarr,next_row))
    return ndarr
