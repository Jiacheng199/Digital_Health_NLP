from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained("medicalai/ClinicalBERT")
model = AutoModel.from_pretrained("medicalai/ClinicalBERT")


raw_inputs = [
    "Sinusitis",
    "Chronic sinusitis",
    "Invasive fungal sinusitis",
    "Complicated acute rhinosinusitis",
    "Uncomplicated acute rhinosinusitis"
]

inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
print(inputs)

outputs = model(**inputs)
print(outputs.last_hidden_state.shape)
print(outputs)
# import tensorflow as tf
# from tensorflow import keras
# # from tensorflow.keras import layers
# # from tensorflow.keras.models import Model


# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# import math
# import secrets


