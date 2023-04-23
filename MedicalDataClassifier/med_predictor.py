import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

#Get the original notes
df = pd.read_csv('MedicalDataClassifier\demo_data.csv', usecols=[0])

# 删除包含NaN值的行
df = df.dropna()

non_medical_data = [
    "apple", "car", "tree", "laptop", "music", "soccer", "chocolate", "coffee",
    "beach", "mountain", "shirt", "computer", "cellphone", "bicycle", "pencil",
    "book", "movie", "television", "dog", "cat"
]
non_medical_df = pd.DataFrame(non_medical_data, columns=["raw"])
non_medical_df["label"] = 0
df = pd.concat([df, non_medical_df], ignore_index=True)
X_train, X_test, y_train, y_test = train_test_split(df["raw"], df["label"], test_size=0.2, random_state=42)

vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

nb_classifier = MultinomialNB()
nb_classifier.fit(X_train_vec, y_train)

y_pred = nb_classifier.predict(X_test_vec)

print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
