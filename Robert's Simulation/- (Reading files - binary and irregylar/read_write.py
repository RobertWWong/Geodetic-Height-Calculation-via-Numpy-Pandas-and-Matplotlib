import numpy as np
import gmes_reader as gmr
import geph_reader as ger
import mrfil_reader as mrr

mrfil = 'MRFIL.asc'
geph = 'geph.eph'
gmes = 'gmes.mes'

# epFile = ger.read_geph_data_frame(geph)
# ep_header, ep_data = epFile
# ger.save_to_text("test_geph1.txt", ep_data)

# npa = []
#
# for i in range(5):
#     npa.append(np.array([i+y for y in range(3)]))
#
#
# npa
#
# t = np.array([[1,2,3],[12,32,42]])
# print(t)

mesFile = gmr.read_gmes_numpy(gmes)
mHead, mLead, mData ,mCleand= mesFile
mData[0]
mData[1]
mData[2]
mData[3]



mCleand.tofile('test_gmes_hell.txt', sep= '\n')


len(mData)
len(mCleand)
# len(mesFile)

# Can't do without proper formatting
# np.savetxt('test_gmes.txt',mData, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ')


mData[0][0]
mCleand[0:3]

ynot = np.vstack(mCleand[0:3])

for i in ynot:
    print(i)



fmt = 'i1,'*4 + 'i4,'*2 + 'f8,'*2 + 'i2'
fmt
nt = np.dtype(fmt)
nt


no = mData[0]
li = []
t = no[0][0]
t
list(t)


np.insert([],slice(0,12), t)

np.concatenate(list(t), axis=0)


np.asarray(no[0][0], dtype = nt)

li.append(no)



np.asarray(mData, dtype=nt)
mData[0]
wat = np.concatenate((mData[0:2],mData[2:10]), axis=0)
wat[0]

mData[19].reshape((1,8))

mData[19].shape
mData[20].shape
np.unique(mData[0])

a = np.array(mData[0:200])
able =np.vstack([[1,2,3],[[2,3,4],[3,4,5],[32,32,12]]])
able[0]
m = mData
m[0]

test = np.array(m[0])
test.


# Hold on, try vstack
np.asarray(a, dtype=nt, order=None)

asd = np.vstack(mData)
asd[0][0][0]

fmt = 'i1,'*4 + 'i4,'*2 + 'f8,'*2 + 'i2'
ntype = np.dtype(fmt)
np_cleaner = np.asarray(asd,dtype = ntype)


asd[0]
ntype



len(mData[19])
len(mData[20])


mData[:10]


mData[0:10]
mCleand[0:100]
mData
# gmr.save_to_txt('test_gmes real.txt',mData)
mLead
#
# mrFile = mrr.read_header_data(mrfil)

# len(mrFile)
# mrFile[0,0]
#
# ep_data#
# mData[0]
