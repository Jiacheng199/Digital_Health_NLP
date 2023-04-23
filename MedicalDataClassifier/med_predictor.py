import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

#Get the original notes
raw_data = pd.read_csv('MedicalDataClassifier\demo_data.csv', usecols=[0])
#get some no relevant data
raw_data2 = pd.read_csv('MedicalDataClassifier\unrelated-data.csv', usecols=[0])

print(raw_data)