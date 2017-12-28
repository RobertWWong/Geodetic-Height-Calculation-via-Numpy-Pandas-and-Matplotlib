import numpy as np
import read_write_geph as rw
import struct as s
import matrix_extraction as me

mrfil = 'MRFIL.ASC'; geph = 'geph.eph'; gmes = 'gmes.mes'

print('Example mrfil file at work')
mrfil_ex = me.variableLoad(mrfil,0)


mrfil_ex[:,0]

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

f1.close()
f1 = open(gmes, 'rb')

# fasd = np.array(1)
# type(fasd)
f1.tell()
f1.seek(80)
ld = np_leader_reader(f1)
ld
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
    return remove_header, np_leader,np_arr



f1.close()


head, a,b = read_gmes_numpy(gmes)
head

a
type(b)
b[0:10]


# Actually do this to make everything better and neatly formatted
# That asarray function really helps
dtype = np.dtype('4i1, 2i4, {}f8,i2'.format(2))
ntype = 'i1,'*4
ntype
ntype += 'i4,'*2
ntype += 'f8,'*2
ntype +='i2'

# Then you can save this data via np.savetxt
f = np.asarray(b,dtype = ntype)
f
np.savetxt('test_gmes2.txt', f, fmt='%.18e', delimiter=' ', newline='n', header='', footer='', comments='# ')


c[61231]

c = np.array(b)
c.shape
d = c[0]
e = d[0]
d[0][0]
e = np.matrix(d[0][0])
e
c
# a[0]
trial = open(gmes, 'rb')
gmes_fmt = '=4b2i2dh'
trial.seek(80+33)
first_data_row = trial.read(30)
first_data_row

translated = s.unpack(gmes_fmt,first_data_row)
translated


# np.savetxt("test_gmes.txt", c)

# Not pretty but it will have to do
c.tofile('test_gmes.txt', sep =" ")

trial.close()
