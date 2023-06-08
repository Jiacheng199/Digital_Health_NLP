from transformers import AutoTokenizer, AutoModel
from scipy import spatial
tokenizer = AutoTokenizer.from_pretrained("medicalai/ClinicalBERT")
model = AutoModel.from_pretrained("medicalai/ClinicalBERT")
import torch
from read_data import read_data
import time
# this is the transformer model  ClinicalBERT F1 = 82.

def autoModel(inputs):
    max_record = 0
    max_name = ""
    tmp_input = tokenizer(inputs, padding=True, truncation=True, return_tensors="pt")
    X = model(**tmp_input)
    count = 0
    for all_resource in range(1, X.last_hidden_state.shape[0]):
        count += 1
        similarity = torch.nn.functional.cosine_similarity(X.last_hidden_state[0], X.last_hidden_state[all_resource])
        t = 0
        for s in similarity:
            t += s

        if t/len(similarity) > max_record:
            max_record = t/len(similarity)
            max_name = inputs[all_resource]

    return max_name, max_record