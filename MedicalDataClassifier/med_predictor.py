import pandas as pd
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import brown
import gensim
import re
from rake_nltk import Rake

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

    # Remove the stop words and punctuation, and join the words back into sentences
    stop_words = set(stopwords.words('english'))
    non_medical_sentences = [' '.join([item for item in sentence if item not in stop_words and item.isalpha()]) for sentence in non_medical_sentences]

    return non_medical_sentences


def generate_keywords(sentences, num_keywords=3, min_words=1, max_words=3):
    rake = Rake(min_length=min_words, max_length=max_words)
    keywords_list = []
    
    for sentence in sentences:
        rake.extract_keywords_from_text(sentence)
        key_words = rake.get_ranked_phrases()[:num_keywords]
        
        # If no keywords found, return the most frequent word as a fallback
        if not key_words:
            words = word_tokenize(sentence)
            if words:
                most_frequent_word = max(set(words), key=words.count)
                key_words.append(most_frequent_word)
            else:
                key_words.append('') # add an empty string if no words in the sentence

        tokenized_key_words = word_tokenize(' '.join(key_words))
        keywords_list.append(tokenized_key_words)

        #remove all the keywords that length is bigger than 4
        keywords_list = [item for item in keywords_list if len(item) <= 4]

    return keywords_list

non_medical_sentences = generate_non_medical_data()
keywords_list = generate_keywords(non_medical_sentences)

print(keywords_list[0:20])
#get the longest keyword
max_len = max([len(item) for item in keywords_list])
print(max_len)

print(keywords_list[0:50])
def save_to_csv(data, file_name):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)