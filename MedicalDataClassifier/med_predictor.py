import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#Get the original notes
test = pd.read_csv('.\Medical_data\demo_data.csv')
train = pd.read_excel('.\Medical_data\simpletabulation.xlsx')

#print the columns
print(train.columns)
#take the 'Title' column only
train['tokens'] = train['Title'].apply(lambda x: word_tokenize(x))
train = train[['tokens']]

#remove the stop words
stop_words = set(stopwords.words('english'))
train['tokens'] = train['tokens'].apply(lambda x: [item for item in x if item not in stop_words])

#remove the punctuation
train['tokens'] = train['tokens'].apply(lambda x: [item for item in x if item.isalpha()])

print("Demo of traing data\n",train.head())