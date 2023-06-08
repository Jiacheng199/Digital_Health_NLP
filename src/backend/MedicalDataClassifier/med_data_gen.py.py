#Description: This code generates medical and non-medical text datasets and combines them together for training a classifier. It also includes functions for generating keywords from sentences using RAKE algorithm, and for saving data to CSV file.
#Note: The model wont be trained in this file

import pandas as pd
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import brown
from rake_nltk import Rake

nltk.download('brown')
# Generate medical data
def generate_medical_data():
    #Get the original notes
    medical_data = pd.read_excel('.\Medical_data\simpletabulation.xlsx')
    #take the 'Title' column only
    medical_data['tokens'] = medical_data['Title'].apply(lambda x: word_tokenize(x))
    medical_data = medical_data[['tokens']]
    #remove the stop words
    stop_words = set(stopwords.words('english'))
    medical_data['tokens'] = medical_data['tokens'].apply(lambda x: [item for item in x if item not in stop_words])
    #remove the punctuation
    medical_data['tokens'] = medical_data['tokens'].apply(lambda x: [item for item in x if item.isalpha()])

    return medical_data

# Generate non-medical data
def generate_non_medical_data():
    # Using the brown corpus
    non_medical_sentences = brown.sents(categories=['news', 'hobbies', 'lore', 'belles_lettres', 'government', 'learned', 'fiction', 'mystery', 'science_fiction', 'adventure', 'romance', 'humor'])

    # Remove the stop words and punctuation, and join the words back into sentences
    stop_words = set(stopwords.words('english'))
    non_medical_sentences = [' '.join([item for item in sentence if item not in stop_words and item.isalpha()]) for sentence in non_medical_sentences]

    return non_medical_sentences

# Generate keywords from sentences
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
        keywords_list = [item for item in keywords_list if len(item) <= 5]

    return keywords_list



# Save data to CSV file, with columns: text, label
def save_to_csv(data, file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["text", "label"])
        writer.writerows(data)


# Generate medical data
non_medical_words = generate_keywords(generate_non_medical_data())

# Create a dictionary to store the tokens and labels
data = {'tokens': non_medical_words, 'label': [0] * len(non_medical_words)}

# Create df from non_medical_words and assign label 0
non_medical_df = pd.DataFrame(data)

# Assign label 1 to medical data
medical_df = generate_medical_data()
medical_df['label'] = 1

#take 10000 rows from non_medical_df and 20000 rows from medical_df to form the training data
non_medical_df = non_medical_df.sample(n=10000, random_state=1)
medical_df = medical_df.sample(n=20000, random_state=1)
combined_df = pd.concat([non_medical_df, medical_df], ignore_index=True)
#shuffle the rows
combined_df = combined_df.sample(frac=1).reset_index(drop=True)
#save the combined_df to csv file, with columns: text, label
save_to_csv(combined_df.values.tolist(), 'combined_data.csv')
