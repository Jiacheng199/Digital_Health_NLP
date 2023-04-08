import os
import uuid
from read_data import read_data

def snomed_ct_dict(exa):
    myuuid = uuid.uuid4()
    cmd = 'mpiexec -n 12 python snomed_ct.py ' + str(myuuid) + ' ' + str(exa)
    os.system(cmd)
    file_name = str(myuuid)+ '.csv'

    read = read_data()
    result = read.read_tmp_ct(file_name)
    # print(result)

    os.remove(str(myuuid)+ '.csv')
    return result

