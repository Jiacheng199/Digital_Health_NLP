import MedicalDataClassifier as mdc
from MedicalDataClassifier.med_data_cls import train_nb_classifier, predict_medical_text

classifier, text_vectorizer = train_nb_classifier()
test_text1 = "[Nice weather]"
result = predict_medical_text(classifier, text_vectorizer, test_text1)
print('Is the Nice weather a medical-related sentence? :', result)

test_text2 = "[pain chest]"
result = predict_medical_text(classifier, text_vectorizer, test_text2)
print('Is the pain chest a medical-related sentence? :', result)

