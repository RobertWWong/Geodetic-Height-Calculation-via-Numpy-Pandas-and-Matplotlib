import numpy as np
import struct as s

# This is the available formatting given a GEPH file.
dRtype = np.dtype("f8,i2,i2,(1,3)i4,(1,10)f4,(1,8)f8")
dLtype = np.dtype("<f8,<i2,<i2,(1,3)<i4,(1,10)<f4,(1,8)<f8")
dBtype = np.dtype(">f8,>i2,>i2,(1,3)>i4,(1,10)>f4,(1,8)>f8")
oneByone = np.dtype("f8,i2,i2,i4,i4,i4,i4,i4,i4,i4,i4,i4,f4,f4,f4,f4,f8,f8,f8,f8,f8,f8,f8,f8")


def read_header_data(fname:str,byte_per_low :int , data_type : int , traditional_reading = False):
        """
        This function will read to a list the first 80 bytes as its header
        It will continue reading the rest of the file in 128 bytes interval, until it reaches an EOF, into an ndarray
        The return type will be a tuple, containing the header byte value and the ndarray
        """

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
            # i = 0
            # fd.seek(80)
            # while fd.readable() and i<100:
            #     try:
            #         buffer_list.append(fd.read(byte_per_low))
            #         if buffer_list[i] == b'':
            #             print("Breaking at {} rows\n".format(i))
            #             buffer_list.pop()
            #             return header,conversion_list
            #
            #         conversion_list.append(np.frombuffer(buffer_list[i],dtype=dtype))
            #     except Exception as e:
            #         raise e
            #     i += 1
