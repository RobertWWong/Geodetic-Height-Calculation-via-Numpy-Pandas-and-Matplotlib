from array import array
import numpy as np


output_file = open('test_bin', 'wb')
float_array = array('d', [159674.609536363])
float_array.tofile(output_file)
output_file.close()

input_file = open('test_bin', 'rb')
float_array = array('d')
float_array.fromfile(input_file,1)
input_file.close()
input_file.closed

float_array

input_file = open('test_bin', 'rb')
input_file.read()
input_file.close()
# with open('test_bin.bin','wb') as wb:
#     fl = [123.1241,5123.12353,3123.534,2164.234]
#
#     farray = array ('d', fl)
#     farray.tofile(wb)
#
#
#
# with open('test_bin.bin','rb') as rb:
#     floatArr = array('d')
#     floatArr.fromstring(rb.read())
#
#     red = rb.read()
#
# # fd = open('test_bin.bin','rb')
# #
# # cont = fd.readline()
# #
# # cont
# # fd.close()
# # fd.closed
# #
# # import st
# # for i in cont:
# #     print(i, chr(i))
