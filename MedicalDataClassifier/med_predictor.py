import pandas as pd
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import brown
nltk.download('brown')

test = pd.read_csv('.\Medical_data\demo_data.csv')

def generate_medical_data():
    #Get the original notes
    train = pd.read_excel('.\Medical_data\simpletabulation.xlsx')
    #take the 'Title' column only
    train['tokens'] = train['Title'].apply(lambda x: word_tokenize(x))
    train = train[['tokens']]
    #remove the stop words
    stop_words = set(stopwords.words('english'))
    train['tokens'] = train['tokens'].apply(lambda x: [item for item in x if item not in stop_words])
    #remove the punctuation
    train['tokens'] = train['tokens'].apply(lambda x: [item for item in x if item.isalpha()])

    return train


def generate_non_medical_data():
    # Using the brown corpus
    non_medical_sentences = brown.sents(categories=['news', 'hobbies', 'lore', 'belles_lettres', 'government', 'learned', 'fiction', 'mystery', 'science_fiction', 'adventure', 'romance', 'humor'])

    # Remove the stop words and punctuation
    stop_words = set(stopwords.words('english'))
    non_medical_sentences = [[item for item in sentence if item not in stop_words] for sentence in non_medical_sentences]
    non_medical_sentences = [[item for item in sentence if item.isalpha()] for sentence in non_medical_sentences]

    # Filter sentences with length between 1 and 3 words
    filtered_sentences = [sentence for sentence in non_medical_sentences if 1 <= len(sentence) <= 3]
    print(filtered_sentences)
    return filtered_sentences
generate_non_medical_data()

def save_to_csv(data, file_name):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)