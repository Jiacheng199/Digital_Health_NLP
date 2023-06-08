import os
import uuid
from read_data import read_data
from snomed_ct import snomed
# this python file is use for SNOMED-CT TEST.
def snomed_ct_dict(exa):
    read_raw = read_data()
    ct = snomed()
    raw = read_raw.read_raw(exa)
    # count = 0
    final_result = {}
    for i in raw.keys():
        pre_data = raw[i]['processed']
        final_result[i] = ct.ct_string_process(pre_data)


    return final_result

