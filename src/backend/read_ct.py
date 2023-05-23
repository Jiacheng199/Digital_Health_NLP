import os
from read_data import read_data

def read_ct_result(uid):
    file_name = str(uid)+ '.csv'
    
    # load raw file
    read = read_data()
    result = read.read_tmp_ct(file_name)
    os.remove(str(uid)+ '.csv')
    return result