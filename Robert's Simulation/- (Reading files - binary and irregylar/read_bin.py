import numpy as np
import matrix_extraction as me

f1 = 'geph.eph'
f2 = 'gmes.mes'


def data_splitter(geph_data):
    start = 0
    geph_amt_per_record = [1,1,1,3,10,8]
    my_list = []
    for i in geph_amt_per_record:
        my_list.append(geph_data[start:start+i])
        start = end
    return my_list
my_list = data_splitter(geph_data)

with open(f2, mode ='rb') as fd:
	header = fd.read(80)
	data_rows = []
	while fd.readable:
		geph_data = s.unpack('dhh3l10f8d', fd.read(128))
		data_rows.append(geph_data)
