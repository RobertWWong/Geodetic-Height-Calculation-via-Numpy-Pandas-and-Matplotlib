from array import array

with open('test_bin.bin','wb') as wb:
    fl = [123.1241,5123.12353,3123.534,2164.234]

    farray = array ('d', fl)
    farray.tofile(wb)



with open('test_bin.bin','rb') as rb:
    floatArr = array('d')
    floatArr.fromstring(rb.read())

    red = rb.read()
