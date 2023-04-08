from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
model = AutoModel.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")


raw_inputs = [
    "Infective exacerbation of asthma",
    "Asthma, infective exacerbation",
    "Acute exacerbation of interstitial lung disease",
    "Bronchiectasis, acute exacerbation",
    "Chronic obstructive pulmonary disease (COPD), acute exacerbation",
    "Cystic fibrosis, acute exacerbation"

]

inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
print(inputs['input_ids'])

X = model(**inputs)
print(X.last_hidden_state[0])
# Y= [
#     "Sinusitis",
#     "Chronic sinusitis",
#     "Invasive fungal sinusitis",
#     "Complicated acute rhinosinusitis",
#     "Uncomplicated acute rhinosinusitis"
# ]
# print(outputs.last_hidden_state.shape)
# print(outputs[0])
# import tensorflow as tf
# from tensorflow import keras
# # from tensorflow.keras import layers
# # from tensorflow.keras.models import Model


# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# import math
# import secrets
import torch

# 创建两个向量
a = torch.tensor([1.0, 2.0])
b = torch.tensor([2.0, 3.0])

# 计算余弦相似度
similarity = torch.nn.functional.cosine_similarity(X.last_hidden_state[0], X.last_hidden_state[1], dim=1)

# print(similarity)  # 输出结果为 tensor(0.9926)
# input1 = torch.(randn(100, 128))
# input2 = torch.randn(100, 128)
# output = torch.nn.functional.cosine_similarity(input1, input2)
# print(output)
t = 0
for i in similarity:
    t += i

print(t/len(similarity))

similarity = torch.nn.functional.cosine_similarity(X.last_hidden_state[0], X.last_hidden_state[2], dim=1)

# print(similarity)  # 输出结果为 tensor(0.9926)
# input1 = torch.(randn(100, 128))
# input2 = torch.randn(100, 128)
# output = torch.nn.functional.cosine_similarity(input1, input2)
# print(output)
t = 0
for i in similarity:
    t += i

print(t/len(similarity))
similarity = torch.nn.functional.cosine_similarity(X.last_hidden_state[0], X.last_hidden_state[3], dim=1)

# print(similarity)  # 输出结果为 tensor(0.9926)
# input1 = torch.(randn(100, 128))
# input2 = torch.randn(100, 128)
# output = torch.nn.functional.cosine_similarity(input1, input2)
# print(output)
t = 0
for i in similarity:
    t += i

print(t/len(similarity))
similarity = torch.nn.functional.cosine_similarity(X.last_hidden_state[0], X.last_hidden_state[4], dim=1)

# print(similarity)  # 输出结果为 tensor(0.9926)
# input1 = torch.(randn(100, 128))
# input2 = torch.randn(100, 128)
# output = torch.nn.functional.cosine_similarity(input1, input2)
# print(output)
t = 0
for i in similarity:
    t += i

print(t/len(similarity))

# print(t/len(similarity))
similarity = torch.nn.functional.cosine_similarity(X.last_hidden_state[0], X.last_hidden_state[5], dim=1)

# print(similarity)  # 输出结果为 tensor(0.9926)
# input1 = torch.(randn(100, 128))
# input2 = torch.randn(100, 128)
# output = torch.nn.functional.cosine_similarity(input1, input2)
# print(output)
t = 0
for i in similarity:
    t += i

print(t/len(similarity))