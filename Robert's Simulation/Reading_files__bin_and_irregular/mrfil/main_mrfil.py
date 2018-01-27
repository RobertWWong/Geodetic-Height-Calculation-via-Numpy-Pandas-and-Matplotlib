import mrfil_reader as mrr

# File name
mrfil = 'MRFIL.ASC'

#Read data
data_row, data_list= mrr.read_header_data(mrfil)

# Saving Data
mrr.save_txt("final_mrfil.txt",data_row)
