import numpy as np



def read_geph_data_frame(fname, skiprows ):
    '''
    Read a geph file into a numpy matrix
    '''
    with open(f1, mode ='rb') as fd:
        header = fd.seek(80)
        print(header)
        i = 0
        npArr = np.fromfile(fd, dtype =dtype)


def data_splitter(geph_data):
    start = 0
    geph_amt_per_record = [1,1,1,3,10,8]
    my_list = []
    for i in geph_amt_per_record:
        my_list.append(geph_data[start:start+i])
        start = start+i
    return my_list
