from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained("medicalai/ClinicalBERT")
model = AutoModel.from_pretrained("medicalai/ClinicalBERT")
import torch
def autoModel(target, inputs):
    raw_resource = []
    for all_inputs in inputs:
        raw_resource.append(all_inputs)

    raw_target = []
    for all in target.keys():
        raw_target.append(target[all])
    # print(inputs)
    max_record = 0
    max_name = ""
    for ii in range(len(raw_target)):
        tmp_list = []
        tmp_list.append(raw_target[ii])
        for jj in range(len(raw_resource)):
            tmp_list.append(raw_resource[jj])
            
        tmp_input = tokenizer(tmp_list, padding=True, truncation=True, return_tensors="pt")
        X = model(**tmp_input)
            # print(all_inputs)
            
        for all_resource in range(1, len(tmp_input)):
            similarity = torch.nn.functional.cosine_similarity(X.last_hidden_state[0], X.last_hidden_state[all_resource], dim=1)
            t = 0
            for s in similarity:
                t += s

            if t/len(similarity) > max_record:
                max_record = t/len(similarity)
                # print(jj)
                # print(processed_list)
                # max_name = processed_list[jj]

    return max_name