import gmes_reader as gmr
import numpy as np
gmes = 'gmes.mes'

head, lead, data, dataC = gmr.read_gmes_numpy(gmes)
data[0]
lmat = np.matrix(lead)

# Function to save numpy arrays exactly to text format, will not preserve data type
gmr.save_to_text('gmes_leader.txt', lead)
gmr.save_to_text('gmes_data.txt', dataC)



# np.savetxt('lead.txt', lmat, fmt = '%s',newline = '\n')
# lead['tmes']

# np.savetxt('lead.txt' ,lmat, newline='\n')
# Don't use np.matrix, it will reorder all the rows from low to high lexiconically.
