import numpy as np
import read_write_geph as rw
import struct as s
import matrix_extraction as me


mrfil = 'MRFIL.ASC'; geph = 'geph.eph'; gmes = 'gmes.mes'

print('Example mrfil file at work')

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
'i1'*4 + 'i4'*2 + 'f8'*2 + 'i2'
# eval ('i1'*4 + 'i4'*2 + 'f8'*2 + 'i2')
type(b)
# Then you can save this data via np.savetxt
f = np.asarray(b,dtype = ntype)
f
np.savetxt('test_gmes2.txt', f, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ')


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
