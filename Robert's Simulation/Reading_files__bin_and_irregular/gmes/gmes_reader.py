import struct as s
import numpy as np


def leader_reader(file ,off_set =0, numpy_array : bool =True):
    '''
    This function will read from a file the leader record of a new frame
    for EVERY NSAT amount of data record rows that it is called upon.
    Every leader record is always 33 bytes long of the format  "ddhh8bb"

    We will be ignoring the first 4 char bytes after the header record, as they are usually binary
    This function will return a 0 if it reaches an EOF or if the format enter is incorrect
    Return a list of relevant data, the Nsat value, and the Nmes value
    '''
    if off_set != 0:
        file.read(off_set)

    if not numpy_array:
        lead_fmt = '=ddhh8bb'  # for struct binary conversions, disregard the sync, it is in its final value state
        lead_size = s.calcsize(lead_fmt)    # This is the amount of bytes read on every function call
        check_bytes = file.read(lead_size)
        if check_bytes == b'' or len(check_bytes) != lead_size:    # Check if we have the correct amount of bytes first. Our format can only accept n amount of bytes
            return 0
        lead_data = s.unpack(lead_fmt,  check_bytes)   # Conversion from bytes to data types

        # Gather necessary data
        data_list = list(lead_data[0:4])        # Transform our converted leader record into a list
        Nsat, Nmes = lead_data[2:4]             # Get our Nsat and Nmes data values
        data_list.append(lead_data[4:4+Nmes])   # Get the Nmes amount of measurement
        data_list.append(lead_data[-1])         # This is the Uiode item value, either a 0 or 1
        return data_list, Nsat, Nmes
    else:
        # Same as above but for the numpy format
        numpy_fmt = np.dtype([('bin','4S'),('tmes','f8'),('dtclk','f8'),('nsat','i2'),('nmes','i2'),('imes','8i1'),('uiode','i1')])
        check_bytes = file.read(33)
        if check_bytes == b'' or len(check_bytes) != 33:
            return 0
        numpy_leader = np.fromstring(check_bytes, dtype=numpy_fmt)
        return numpy_leader

def data_reader(bufferStream, nsat :int , nmes :int, off_set =0):
    '''
    This function will read Nsat amount of rows from a gmes file and put them into the appropriate format
    Given Nsat and Nmes data value from the leader record, the function will read at most
    (14 + nmes*8 bytes ) x Nsat amount of time per data frame.

    SIDE NOTE: What is returned IS A type numpy.ndarray BUT because it has be customly formatted,
    it IS ACTUALLY is the type numpy.void. This is important because formatting files will become much more difficult as
    regular numpy.savetxt will not work due to the numpy.void nature.

    You are highly advised to access the array by field name  if you want a column vector. Regular matlab conventions do not apply for this class
    ie matrix['f0'] where f0 is the first column
    '''
    if off_set !=0:
        bufferStream.seek(bufferStream.tell() + off_set)

    read_size = 14+nmes*8       # Current size of our byte structure

    #This is the format to which we will save our file to
    fmt = 'i1,'*4 + 'i4,'*2 + 'f8,'*nmes + 'i2'
    dtype = np.dtype(fmt)
    # dtype = np.dtype('4i1, 2i4, {}f8,i2'.format(nmes))                 # This is our seconday format for a gmes data record


    ndarr = np.fromstring(bufferStream.read(read_size), dtype=dtype)    # np function to convert byte buffer to their respective numpy data type
    vstack_later = []
    for i in range(nsat-1):     # Now append to the matrix the rest of the data frames' rows
        next_row = np.fromstring(bufferStream.read(read_size), dtype=dtype)
        vstack_later.append(next_row)
    ndarr = np.vstack((ndarr,vstack_later))
    return ndarr


def read_gmes_numpy(fname):
    with open (fname, 'rb') as fgmes:
        Mose7_header = fgmes.read(80)      # This will read our Moses header

        leader = leader_reader(fgmes)    # Get our leader record array
        np_leader = [leader]            # we add our Leader record last, so start the list with the current leader
        np_arr = []
        print('stage 1 reading initial Leader record to populate Nsat and Nmes values for the Data Record')
        while type(leader) != int:
            nsat,nmes = leader['nsat'][0], leader['nmes'][0]    #Get our necessary values

            data_set = data_reader(fgmes, nsat, nmes)   # Get our Data record set and add it to the temp numpy arr
            np_arr.append(data_set)

            leader = leader_reader(fgmes)    # Get our new leader record to read the next nsat rows
            if type(leader) != int:         # Only append to our list the leader record when there is a valid byte to read in the file buffer
                np_leader.append(leader)
            else:
                print("Done Reading till gmes EOF")
    print("End stage")

    # We will now take all our leader records and stack them all into one numpy array
    np_leader = np.vstack((np_leader[0],np_leader[1:]))

    # This will convert our data record into one convienent numpy array
    # We will lose our data frame but we now have an array of neatly stacked values
    np_clean = np.vstack(np_arr)
    return Mose7_header, np_leader,np_arr, np_clean


def save_to_text (fname, npArr):
    '''
    This will take a unformatted np_clean and write the content of the matrix into a file
    If i attempt to reformat my array type, it will screw up the row order.
    '''
    #This is the format to which we will save our file to
    npArr.tofile(fname, sep= '\r\n')



def demo_gmes_reader():
    '''
    This is a demo function to show working functionality of reading a binary gmes file
    into a numpy array
    '''

    gmes = 'gmes.mes'
    mesFile = read_gmes_numpy(gmes)
    mHead, mLead, mData ,mCleand= mesFile   # This is called unpacking. Very useful if you hae a list of list, where each variable can be assigned to each inner element, provided you have enough variables

    save_to_text('test_gmes_clean.txt', mCleand, newline='\r\n')
    save_to_text('test_gmes_lead', mLead, newline='\r\n')

    # This will preserve our numpy data type in a special binary numpy file
    np.save('nump_lead',mLead)
    np.save('nump_data',mCleand)
    return mHead, mLead, mData ,mCleand
