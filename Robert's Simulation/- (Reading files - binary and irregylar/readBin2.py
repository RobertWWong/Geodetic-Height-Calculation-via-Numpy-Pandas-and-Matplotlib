import numpy as np
import matrix_extraction as me
import struct as s
import array

def data_splitter(geph_data):
    start = 0
    geph_amt_per_record = [1,1,1,3,10,8]
    my_list = []
    for i in geph_amt_per_record:
        my_list.append(geph_data[start:start+i])
        start = start+i
    return my_list

f1 = 'geph.eph'
f2 = 'gmes.mes'

#Using numpy to convert binary to their respective format. It works, but time is still out of range
print("#ANOTHER THING, IS BYTE LITTLE ENDIAN OR BIG ENDIAN?")

dRtype = np.dtype("f8,i2,i2,(1,3)i4,(1,10)f4,(1,8)f8")
dLtype = np.dtype("<f8,<i2,<i2,(1,3)<i4,(1,10)<f4,(1,8)<f8")
dBtype = np.dtype(">f8,>i2,>i2,(1,3)>i4,(1,10)>f4,(1,8)>f8")

oneByone = np.dtype("f8,i2,i2,i4,i4,i4,i4,i4,i4,i4,i4,i4,f4,f4,f4,f4,f8,f8,f8,f8,f8,f8,f8,f8")


# It might be little endian
dtype = dRtype
# List to keep record of bytes and formats read and converted
buffer_list = []
conversion_list = []
np.set_printoptions(precision=12)
#Let's try to do bytes to integer
# READ F1
with open(f1, mode ='rb') as fd:
    header = fd.seek(80)
    print(header)
    i = 0
    npArr = np.fromfile(fd, dtype =dtype)
    fd.seek(80)
    while fd.readable() and i<100:
        try:
            if i == -1:
                nparr = np.ndarray(dtype = dtype, buffer = buffer(fd.read())  )
                fd.seek(80)

            buffer_list.append(fd.read(128))
            if buffer_list[i] == b'':
                print("Breaking at {}\n".format(i))
                break
            conversion_list.append(np.frombuffer(buffer_list[i],dtype=dtype))
        except Exception as e:
            print('we done now  ', e)
            raise e
        i += 1


# Saving file via numpy
fmt_dict = {'1':'f', '2':'d', '3':'d', '10':'e', '8':'e'}
for i in fmt_dict.items():
    print(i)

fmt =""
def all_split():
    for amt,typ in fmt_dict.items():
        for i in range(int(amt)):
            padding =6
            if typ =='e':
                padding = 15
            fmt += "%{pad}{typ}".format(typ = typ, pad=padding)
    return fmt

fmt = all_split()

np.savetxt("geph_test.txt", npArr, fmt=fmt)

type(npArr[0])


conversion_list[0]

len(buffer_list[-2])
temp_fmt = "d"
some_data = s.unpack(temp_fmt, buffer_list[1][:8])
some_data


#Attempting matrix  creation via np.frombuffer



# a = open(f1,mode='rb')
# a.read()
# a.seek(80)
# for i in a:
#     print(i)
# a.readline()
# a.readable()
# a.close()


# len(conversion_list)
#
# print(conversion_list[0])
# conversion_list[1]
# conversion_list[2]
# conversion_list[3]
# conversion_list[4]


print('I THINK I NEED STRUCT MODULE AFTER ALL')
print("https://stackoverflow.com/questions/5415/convert-bytes-to-floating-point-numbers-in-python")
conversion_list[34]

# I don't understand the format of 2?
# Oh no, f is our 4 byte float representation
# d is our 8 byte float representation

geph_format = 'dhh3i10f8d'
print("https://docs.python.org/3/library/struct.html")


# first_data[0:8]
# type(first_data[0:8])
geph_data = s.unpack(geph_format, conversion_list[0])

gdata = data_splitter(geph_data)
gdata
#
# data_cluster = []
# data_cluster.append(geph_data[0])
# data_cluster.append(geph_data[1])
# data_cluster.append(geph_data[2])
# data_cluster.append(tuple(geph_data[3:6]))
# data_cluster.append(tuple(geph_data[7:17]))
# data_cluster.append(tuple(geph_data[17:25]))
#
# data_cluster[0]
# data_cluster[1]
# data_cluster[2]
# data_cluster[3]
# data_cluster[4]
# data_cluster[5]
# len(first_data[0:8])


# # Proper formating of our data splitting now
# my_list = data_splitter(geph_data)
# my_list
# print("ok this works for sure")
# myList2 = data_splitter(geph_second_row)
#
# second_data
#
# geph_second_row =s.unpack('dhh3l10f8d', second_data)
# three = data_splitter(s.unpack('dhh3l10f8d', third))
# four = data_splitter(s.unpack('dhh3l10f8d', fourth))
# five = data_splitter(s.unpack('dhh3l10f8d', fifth))
#
# three
# four
#
# five
# for i in range(len(myList2)):
#     print("{firstrow}   vs     {secondrow}\n".format(firstrow=1, secondrow= myList2[i]))
#

# lines[0]
#
# lines[0][:80]
# lines[0][80:160]
# bin_list = lines[0].split()
#
# bin_list[0]
#



# # Unsigned big endian int
# print( int.from_bytes(bin_list[3], byteorder='big'))

# # Unsigned little endian int
# print( int.from_bytes(bin_list[3], byteorder='little'))

# i = int.from_bytes(lines[0], byteorder='big')
# print(i)

# # Use codec to deal with base 64 encodings
# # Failed
# import codecs
# # codecs.decode(bin_list[3])



# # Attempt at figuring out char from int in geph
# import sys
# from functools import partial

# chunk_size = 1
# with open(f1, 'rb') as in_file:
#     for data in iter(partial(in_file.read, chunk_size), b''):
#         x = int.from_bytes(data, byteorder='big')
#         if (x < 64 and x < 91) or (x < 96 and x < 123) :
#             sys.stdout.write(chr(x))
#         else:
#             sys.stdout.write('.')


# # The array function can read binary values into array, but I don't know how accurate
# # Our geph files is an nx8 matrix i think
# import array
# with open(f1,mode = 'rb') as fbin:
# 	a = array.array("L")
# 	a.fromfile(fbin, 8)
# a[0]

# with open(f1, mode='rb') as fid:
#     data_a = np.fromfile(fid,np.uint16).reshape((8,-1)).T

# data_a[0:10,0]
# data_a[0:10,1]
# data_a[0:10,2]
# data_a[0:10,3]


# data_a[0:10]

# bin_list[0]


# # with open(f2,mode = 'rb') as fd:
# # 	gp2 = np.fromfile(fd)
# #
# #
# # gp2[0:10]
