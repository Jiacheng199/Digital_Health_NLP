#Description: This file is used to train the model and predict the label for the medical data, to classify whether the input raw text is legit medical text or not.
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

# Train the model and a simple evaluation
def train_nb_classifier():
    train_data = pd.read_csv('MedicalDataClassifier/Medical_data/med_cls_train.csv')
    
    #split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        train_data['text'], train_data['label'], test_size=0.1, random_state=42
    )

    #vectorize the text first
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    #using the Multinomial Naive Bayes classifier
    clf = MultinomialNB()
    clf.fit(X_train_vec, y_train)
    
    return clf, vectorizer

# Predict the label for a raw text
def predict_medical_text(clf, vectorizer, raw_text):
    raw_text_vec = vectorizer.transform([raw_text])
    label = clf.predict(raw_text_vec)
    return bool(label[0])

# Run tests on the trained model
def run_tests(clf, vectorizer):
    test_data = pd.read_csv('MedicalDataClassifier/Medical_data/med_cls_test.csv')
    X_test = test_data['text']
    y_test = test_data['label']

    # Vectorize the test text
    X_test_vec = vectorizer.transform(X_test)

    # Make predictions
    y_pred = clf.predict(X_test_vec)

    # Calculate accuracy and f1 score
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')

    print('Test Accuracy: ', accuracy)
    print('Test F1 score: ', f1)

# Usage example
if __name__ == '__main__':
    classifier, text_vectorizer = train_nb_classifier()
    test_text = "['heart', 'pain']"
    result = predict_medical_text(classifier, text_vectorizer, test_text)


