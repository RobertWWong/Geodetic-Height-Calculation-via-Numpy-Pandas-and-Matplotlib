import numpy as np
import matrix_extraction as me

f1 = 'geph.eph'
f2 = 'gmes.mes'

#Let's try to do bytes to integer
with open(f2, mode ='rb') as fd:
    header = fd.read(80)
    print(header)
    first_data = fd.read(128)
    second_data = fd.read(128)
    third = fd.read(128)
    fourth = fd.read(128)
    fifth =  fd.read(128)
header
first_data
second_data
third

print('I THINK I NEED STRUCT MODULE AFTER ALL')
print("https://stackoverflow.com/questions/5415/convert-bytes-to-floating-point-numbers-in-python")
import struct as s

# I don't understand the format of 2?
# Oh no, f is our 4 byte float representation
# d is our 8 byte float representation

geph_format = 'dHH3I10f8d'
print("https://docs.python.org/3/library/struct.html")


first_data[0:8]
type(first_data[0:8])
# geph_data = s.unpack('dhh3l10f8d', first_data)
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
#

# Proper formating of our data splitting now
def data_splitter(geph_data):
    start = 0
    geph_amt_per_record = [1,1,1,3,10,8]
    my_list = []
    for i in geph_amt_per_record:
        my_list.append(geph_data[start:start+i])
        start = start+i
    return my_list
my_list = data_splitter(geph_data)

my_list
print("ok this works for sure")

geph_second_row =s.unpack('dhh3l10f8d', second_data)
myList2 = data_splitter(geph_second_row)
three = data_splitter(s.unpack('dhh3l10f8d', third))
four = data_splitter(s.unpack('dhh3l10f8d', fourth))
five = data_splitter(s.unpack('dhh3l10f8d', fifth))

three
four

five
for i in range(len(myList2)):
    print("{firstrow}   vs     {secondrow}\n".format(firstrow=1, secondrow= myList2[i]))


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
#         if (x > 64 and x < 91) or (x > 96 and x < 123) :
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
