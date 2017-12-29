import geph_reader as ger

geph = 'geph.eph'
fout = 'geph_test1.txt'

epFile = ger.read_geph_data_frame(geph)
ep_header, ep_data = epFile
ger.save_to_text(fout, ep_data)


