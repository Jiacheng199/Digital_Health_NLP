# Development for sprint2(future sptrint3 possible)

This branch is for developing mapping data modification,login/register pages for now(US05 and US08) and medical data classification using Naive Bayes classifier.

This branch will be merged into the milestone branch using either the merge or manual copy method.

## How to test the front-dev of this project
Since we need to load the mock data to perform the mapping data modification testing, so one way to testing the current branch is to run 
python code: `python -m http.server`; This will allow you to run the project on localhost:8000.

## How to use the medical data classification function in other code
First, ensure that you have the required Python libraries installed:

`pip install pandas scikit-learn nltk rake_nltk numpy`

Usage:
Train the classifier using the training dataset:
`classifier, text_vectorizer = train_nb_classifier()`

Use the predict_medical_text function to predict whether the input text is medical-related:

`result = predict_medical_text(classifier, text_vectorizer, test_text)`

`print('Is the text medical-related? :', result)`

## NOTE
Part of this sprint is only a front-end project, but able to get the data from input. logical operation should not be implemented in this sprint branch,.