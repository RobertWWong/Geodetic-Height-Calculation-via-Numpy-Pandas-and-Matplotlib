import matrix_extraction as me

f1 ='YSFIL.ASC'
m1 = me.loadfile(f1, skiprows =3)

m1[:,0]

m2 = me.genload_file(f1, delimiter=None, skip_header=3, skip_footer=0, names =True)
