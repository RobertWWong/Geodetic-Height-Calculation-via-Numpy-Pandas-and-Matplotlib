import numpy as np
import read_write_geph as rw
import struct as s

geph = 'geph.eph'
gmes = 'gmes.mes'

# # head, row = rw.read_header_data(geph, 128 , 4, traditional_reading = False)
# #
# # row['f0']   # You can access the first column by the field name of the data type, like this
# #       # dtype=[('f0', '<f8'), ('f1', '<i2'), ('f2', '<i2'), ('f3', '<i4', (1, 3)), ('f4', '<f4', (1, 10)), ('f5', '<f8', (1, 8))])
# # # rw.write_np_txt('test.txt',row)
# fmes = open(gmes,'rb')
# head = fmes.read(80)
# # unnecessary_bytes= fmes.seek(84)
# #
# #
# #
# # gmes_split = [4,4,8,8,8,8,8,8,16,8]
# # wat = rw.data_splitter(head, gmes_split)
# # wat
# # # lead_fmt = 'ddhh8bb'
# # # s.calcsize(lead_fmt)
#
# fmes.seek(80)
# fmes.tell()
#
# # a = (fmes.read(33))
# numpy_fmt = np.dtype([('bin','4S'),('tmes','f8'),('dtclk','f8'),('nsat','i2'),('nmes','i2'),('imes','8i1'),('uiode','i1')])
# b = np.fromstring(fmes.read(33), dtype=numpy_fmt)
#
# b['tmes']
#
# fmes.tell()
# # fmes.seek(113 + 1*9*30)
# fmes.seek(80)
#
# lead_fmt = '=4cddhh8bb'  # for struct binary conversions, disregard the sync, it is in its final value state
# read_size = s.calcsize(lead_fmt)
# lead_data = s.unpack(lead_fmt, fmes.read(read_size))
#
#
# def gmes_leader_splitter(byte_stream):
#     '''
#     The leader record is always 33 bytes long.
#     '''
#
#     lead_fmt = '=4cddhh8bb'  # for struct binary conversions, disregard the sync, it is in its final value state
#     read_size = s.calcsize(lead_fmt)
#     lead_data = s.unpack(lead_fmt, byte_stream.read(read_size))
#
#     # Populate our list with the first four items of the gmes leader record
#     #Get the nmes count of our future files
#     ret_list = list(lead_data[0:5])
#     nmes = ret_list[4]
#
#     #Populate it with the next nmes in the list
#     ret_list.append(lead_data[5:5+nmes])
#     #Add in the Uiode item value
#     ret_list.append(lead_data[-1])
#
#     print("Here is our leader record: " , lead_data)
#
#     return ret_list,nmes
# fmes.seek(84+33+9*30)
# mes_list,nmes = gmes_leader_splitter(fmes,0)
# nmes
# mes_list
#
#
# print('YES, I NEED TO RUN THE FUNCTION AGAIN FOR A NEW LEADER RECORD AFTER Nsat AMOUNT OF ROWS READ.')
# print("AFTER THAT, I AM DONE. JESUS")
#
# def gmes_data_record(fileStream, nmes: int, use_nparr = False):
#     '''
#     Gmes data record hold at least 14 + nmes*8 bytes per row.
#     '''
#     # Python very picky, need to put alignment to fmt otherwise calcsize of the fmt
#     # will not be exact (fmt will want to fit with a 2^n bytes)
#     # That is  what the = stand for
#
#     fileStream.seek(80+33)  # The data starts after the Header and Leader record
#     gmes_fmt = '=4b2i{}dh'.format(nmes)
#     size = s.calcsize(gmes_fmt)
#     print(size)
#     bufferStream = fileStream.read(size)
#     ret_list = []
#     while bufferStream != b'':
#         if len(bufferStream) != size:
#             print ('Somethings off')
#             print(len(bufferStream), bufferStream)
#             return ret_list
#         ret_list.append(s.unpack(gmes_fmt, bufferStream))
#         bufferStream = fileStream.read(size)
#     return ret_list
#
# ######################################
# #Separation to true functions
#
# numpy_fmt = np.dtype([('bin','4S'),('tmes','f8'),('dtclk','f8'),('nsat','i2'),('nmes','i2'),('imes','8i1'),('uiode','i1')])
# b = np.fromstring(fmes.read(33), dtype=numpy_fmt)

def np_leader_reader(file ):
    try:
        numpy_fmt = np.dtype([('bin','4S'),('tmes','f8'),('dtclk','f8'),('nsat','i2'),('nmes','i2'),('imes','8i1'),('uiode','i1')])
        byte_val = file.read(33)
        if byte_val == b'' or len(byte_val) != 33:
            print("Leader is at EOF or incorrect byte length: ", len(byte_val))
            return 0

        numpy_header = np.fromstring(byte_val, dtype=numpy_fmt)
        return numpy_header
    except Exception as e:
        print("Problem in leader reader")
        raise e

def np_record_data(bufferStream,nsat, nmes, off_set = 0):
    """
    In the case that we want a numpy array (probably better)
    bytes read are 14 + nmes * 8 bytes
    """
    if off_set !=0:
        bufferStream.seek(bufferStream.tell() + off_set)
    read_size = 14+nmes*8
    dtype = np.dtype('4i1, 2i4, {}f8,i2'.format(nmes))
    try:
        byteVal = bufferStream.read(read_size)
        if byteVal ==b'' or len(byteVal) != read_size:
            print('Data record EOF or incorrect byte length: ',len(byteVal))
            return 0

        ndarr = np.fromstring(byteVal, dtype=dtype)
        ndarr = [ndarr]
        for i in range(nsat-1):
            next_row = np.fromstring(bufferStream.read(read_size), dtype=dtype)
            ndarr = np.vstack((ndarr,next_row))
            # ndarr.append(next_row)
        return ndarr

    except Exception as e:
        print("Problem in record data ")
        raise e


    # Checking for an end of file
# fmes.seek(80+33)
# fmes.tell()
#
# what = [[i for i in range(3)] for j in range(3)]
#
# n1 = np.array(what)
# n2 = np.array(what)*2
# n1
# n2
# arr = np_record_data(fmes, b['nsat'][0], b['nmes'][0])
# arr['f0']
#
# # this is to stack them up
# n1 = np.array(1)
# n2 = np.array(2)
# n1,n2
#
# n2 = n1
#
# n1 = np.array(232)
# n1
f1.close()
f1 = open(gmes, 'rb')

# fasd = np.array(1)
# type(fasd)
f1.tell()
f1.seek(80)
# ld = np_leader_reader(f1)
# ld
#
# nsat = ld['nsat'][0]
# nmes = ld['nmes'][0]
# nsat
# data = np_record_data(f1, nsat, nmes, off_set = 0)
# data
#
# type(ld) is not int
# type( ld )is np.ndarray


f1.seek(80)
ap = []
ab = []

for i in range(67434):
    ld = np_leader_reader(f1)
    ap.append(ld)
    # print(type(ld), ld)
    if type(ld) is not np.ndarray :
        print("oh no not like this ",i)
        break
    # print(ld)
    nsat = ld['nsat'][0]
    nmes = ld['nmes'][0]
    nsat
    data = np_record_data(f1, nsat, nmes, off_set = 0)
    ab.append(data)
ld
data


len(ap)
ap[1:10]
ass = np.vstack((ap[0],ap[1:]))
ass['bin']

ab[0]
ab[0:1]

a1 = np.vstack(([ab[0]], ab[1:4]))
a1

ab[0].shape
ab[1:2][0].shape

ab[0][0]
ab[0][0]


def read_gmes_numpy(fname):
    with open (fname, 'rb') as fgmes:
        remove_header = fgmes.read(80)
        # Get our leader recprd array
        leader = np_leader_reader(fgmes)

        np_leader = [leader]
        np_arr = []
        print('stage 1')
        while type(leader) != int:
            #Get our necessary values
            nsat,nmes = leader['nsat'][0], leader['nmes'][0]

            # Get our Data record set and add it to the temp numpy arr
            data_set = np_record_data(fgmes, nsat, nmes, off_set = 0)
            np_arr.append(data_set)

            # Get our new leader record to read the next nsat rows
            leader = np_leader_reader(fgmes)
            if type(leader) != int:
                np_leader.append(leader)
            else:
                print("That's a big file")
    print("End stage")
    print(np_leader[0],'\n',np_leader[-1])
    print()
    print(np_arr[0],'\n\n',np_arr[-1])

    np_leader = np.vstack((np_leader[0],np_leader[1:]))
    # np_arr = np.vstack((np_arr[0],np_arr[1:]))
    return np_leader,np_arr



f1.close()
#
a,b = read_gmes_numpy(gmes)
a.shape
type(b)

c = np.array(b)
c.shape

c
# a[0]

e44 = np.eye(8, M=4, k=0, dtype=float)
e44 *=2

e54 = np.eye(5, M=4, k=0, dtype=float)

ass = np.concatenate((e44,e54), axis =0)
ass


       array([[([32,  0, 48,  0], [1, 0], [ -6.16304494e+06,   1.70222168e+01], 1)],
       [([18,  0, 38,  0], [1, 0], [ -4.04565447e+06,   3.40324707e+01], 1)],
       [([31,  0, 39,  0], [1, 0], [ -4.83943812e+06,  -6.02978516e+01], 1)],
       [([ 8,  0, 38,  0], [1, 0], [ -2.98109122e+06,   3.09228516e+01], 1)],
       [([27,  0, 32,  0], [1, 0], [ -2.71870769e+06,   5.18698730e+01], 0)],
       [([24,  3, 20,  0], [0, 0], [  0.00000000e+00,   0.00000000e+00], 0)],
       [([ 1,  0, 41,  0], [1, 0], [ -2.59702150e+06,  -6.27802734e+01], 0)],
       [([14,  0, 43,  0], [1, 0], [ -6.16223372e+06,  -2.91918945e+00], 0)],
       [([10,  0, 46,  0], [1, 0], [ -5.71224747e+06,   1.74355469e+01], 0)]],
      dtype=[('f0', 'i1', (4,)), ('f1', '<i4', (2,)), ('f2', '<f8', (2,)), ('f3', '<i2')]),
       array([[([32,  0, 48,  0], [2, 0], [ -6.16302791e+06,   1.70354004e+01], 1)],
       [([18,  0, 38,  0], [2, 0], [ -4.04562041e+06,   3.40480957e+01], 1)],
       [([31,  0, 39,  0], [2, 0], [ -4.83949841e+06,  -6.02919922e+01], 1)],
       [([ 8,  0, 38,  0], [2, 0], [ -2.98106028e+06,   3.09169922e+01], 1)],
       [([27,  0, 32,  0], [2, 0], [ -2.71865581e+06,   5.18835449e+01], 0)],
       [([24,  3, 20,  0], [0, 0], [  0.00000000e+00,   0.00000000e+00], 0)],
       [([ 1,  0, 41,  0], [2, 0], [ -2.59708428e+06,  -6.27714844e+01], 0)],
       [([14,  0, 43,  0], [2, 0], [ -6.16223666e+06,  -2.92993164e+00], 0)],
       [([10,  0, 46,  0], [2, 0], [ -5.71223003e+06,   1.74433594e+01], 0)]],
      dtype=[('f0', 'i1', (4,)), ('f1', '<i4', (2,)), ('f2', '<f8', (2,)), ('f3', '<i2')]),
       array([[([32,  0, 48,  0], [3, 0], [ -6.16301088e+06,   1.70375977e+01], 1)],
       [([18,  0, 38,  0], [3, 0], [ -4.04558638e+06,   3.40537109e+01], 1)],
       [([31,  0, 39,  0], [3, 0], [ -4.83955872e+06,  -6.02919922e+01], 1)],
       [([ 8,  0, 38,  0], [3, 0], [ -2.98102934e+06,   3.09377441e+01], 1)],
       [([27,  0, 32,  0], [3, 0], [ -2.71860394e+06,   5.18647461e+01], 0)],
       [([24,  3, 20,  0], [0, 0], [  0.00000000e+00,   0.00000000e+00], 0)],
       [([ 1,  0, 41,  0], [3, 0], [ -2.59714706e+06,  -6.27780762e+01], 0)],
       [([14,  0, 43,  0], [3, 0], [ -6.16223959e+06,  -2.93066406e+00], 0)],
       [([10,  0, 46,  0], [3, 0], [ -5.71221259e+06,   1.74453125e+01], 0)]],
      dtype=[('f0', 'i1', (4,)), ('f1', '<i4', (2,)), ('f2', '<f8', (2,)), ('f3', '<i2')]),
       ...,
       array([[ ([11,  0, 37,  0], [22868,     0], [ -3.65530403e+06,   3.35178223e+01], 1)],
       [ ([26,  0, 37,  0], [ 7833,     0], [ -3.10184466e+06,  -5.57297363e+01], 1)],
       [ ([31,  0, 45,  0], [66731,     0], [ -6.64095203e+06,   1.41425781e+01], 1)],
       [ ([25,  0, 28,  0], [  176,     0], [ -2.55741341e+06,   1.61147461e+01], 1)],
       [ ([32,  0, 43,  0], [66659,     0], [ -4.06636081e+06,   3.90437012e+01], 0)],
       [ ([ 1,  0, 37,  0], [12801,     0], [ -5.02547612e+06,   4.46289062e-01], 0)],
       [ ([ 3,  0, 39,  0], [20071,     0], [ -3.61292384e+06,  -5.63728027e+01], 0)],
       [ ([10,  0, 34,  0], [28129,     0], [ -3.26788316e+06,   5.55944824e+01], 0)],
       [ ([22,  0, 42,  0], [20535,     0], [ -4.99145412e+06,  -4.33203125e+01], 0)]],
      dtype=[('f0', 'i1', (4,)), ('f1', '<i4', (2,)), ('f2', '<f8', (2,)), ('f3', '<i2')]),
       array([[ ([11,  0, 37,  0], [22869,     0], [ -3.65527053e+06,   3.35036621e+01], 1)],
       [ ([26,  0, 37,  0], [ 7834,     0], [ -3.10190041e+06,  -5.57407227e+01], 1)],
       [ ([31,  0, 45,  0], [66732,     0], [ -6.64093791e+06,   1.41262207e+01], 1)],
       [ ([25,  0, 28,  0], [  177,     0], [ -2.55739728e+06,   1.61022949e+01], 1)],
       [ ([32,  0, 43,  0], [66660,     0], [ -4.06632178e+06,   3.90393066e+01], 0)],
       [ ([ 1,  0, 37,  0], [12802,     0], [ -5.02547569e+06,   4.44824219e-01], 0)],
       [ ([ 3,  0, 39,  0], [20072,     0], [ -3.61298019e+06,  -5.63564453e+01], 0)],
       [ ([10,  0, 34,  0], [28130,     0], [ -3.26782756e+06,   5.55817871e+01], 0)],
       [ ([22,  0, 42,  0], [20536,     0], [ -4.99149744e+06,  -4.33154297e+01], 0)]],
      dtype=[('f0', 'i1', (4,)), ('f1', '<i4', (2,)), ('f2', '<f8', (2,)), ('f3', '<i2')]),
       array([[ ([ 1,  0, 37,  0], [12803,     0], [ -5.02547525e+06,   4.42871094e-01], 0)],
       [ ([ 3,  0, 39,  0], [20073,     0], [ -3.61303656e+06,  -5.63786621e+01], 0)],
       [ ([10,  0, 34,  0], [28131,     0], [ -3.26777200e+06,   5.55715332e+01], 0)],
       [ ([22,  0, 42,  0], [20537,     0], [ -4.99154075e+06,  -4.33200684e+01], 0)]],
      dtype=[('f0', 'i1', (4,)), ('f1', '<i4', (2,)), ('f2', '<f8', (2,)), ('f3', '<i2')])], dtype=object)
