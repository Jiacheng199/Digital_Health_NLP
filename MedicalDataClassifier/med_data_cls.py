import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

train_data = pd.read_csv('./Medical_data/med_cls_train.csv')

#using 9:1 ratio for train:test
X_train, X_test, y_train, y_test = train_test_split(
    train_data['text'], train_data['label'], test_size=0.1, random_state=42
)

#vectorize the text
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

#using Multinomial Naive Bayes
clf = MultinomialNB()
clf.fit(X_train_vec, y_train)

y_pred = clf.predict(X_test_vec)
#accuracy and f1 score
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='weighted')
print('Accuracy: ', accuracy)
print('F1 score: ', f1)


#test on the demo data set
demo_data = pd.read_csv('./Medical_data/demo_data.csv')
demo_data_vec = vectorizer.transform(demo_data['raw'])
#predict the label
demo_data['label'] = clf.predict(demo_data_vec)
#print the label 1 ratio
print('Label 1 ratio: ', demo_data['label'].sum()/len(demo_data['label']))


