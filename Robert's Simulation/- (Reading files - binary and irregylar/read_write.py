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



mesFile = gmr.read_gmes_numpy(gmes)
# len(mesFile)
mHead, mLead, mData ,mCleand= mesFile

# Can't do without proper formatting
np.savetxt('test_gmes.txt',mData, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ')

np.tofile


len(mLead)
len(mData)
len(mCleand)
fmt = 'i1,'*4 + 'i4,'*2 + 'f8,'*2 + 'i2'
fmt

nt = np.dtype(fmt)
np.asarray(mData, dtype=nt)


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
