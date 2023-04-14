from transformers import AutoTokenizer, AutoModel
from scipy import spatial
tokenizer = AutoTokenizer.from_pretrained("medicalai/ClinicalBERT")
model = AutoModel.from_pretrained("medicalai/ClinicalBERT")
import torch
from read_data import read_data
from mpi4py import MPI
import time
# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# size = comm.Get_size()
def autoModel(inputs):
    max_record = 0
    max_name = ""
    # source = []
    # source.append(target)
    # for i in inputs.keys():
    #     source.append(i)

    start_time = time.time()
    # print(len(inputs))
    tmp_input = tokenizer(inputs, padding=True, truncation=True, return_tensors="pt")
    X = model(**tmp_input)
    # print(time.time())
        # print(all_inputs)
    count = 0
    # print(X.last_hidden_state.shape[0])
    for all_resource in range(1, X.last_hidden_state.shape[0]):
        count += 1
        # print(count)
        # if count % size != rank:
        #     continue
        # print(time.time() - start_time)
        similarity = torch.nn.functional.cosine_similarity(X.last_hidden_state[0], X.last_hidden_state[all_resource])
        t = 0
        # print(time.time() - start_time)
        # print(similarity)
        for s in similarity:
            t += s

        if t/len(similarity) > max_record:
            max_record = t/len(similarity)
            max_name = inputs[all_resource]
        # break
    # print(max_record)

    return max_name, max_record



# import sys
# ex = sys.argv[1]
# import pandas as pd
# read_raw = read_data()
# raw = read_raw.read_raw(ex)
# final_result = {}
# traget_list = []

# for i in raw.keys():
#     pre_data = raw[i]['processed']
#     tmp = ""
#     for j in pre_data:
#         tmp+=j[0]
#         tmp+=" "
#     traget_list.append(tmp[:-1])

# uil_list = read_raw.read_uil_list()
# all_uil = []
# for i in uil_list:
#     all_uil.append(i[0])

# pending_list = []
# for tmp_list in traget_list:

#     pending_list.append(tmp_list)
#     for all_uil_tmp in all_uil:
#         pending_list.append(all_uil_tmp)
#     break

# autoModel(pending_list)

# autoModel(["Results follow up - left message","bacterial prophylaxis following lung transplant"])
