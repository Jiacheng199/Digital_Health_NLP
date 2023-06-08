# Running Enriovemnt (development only)
pip install nltk pymysql bcrypt jwt torch scipy
pip install spacy
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_bionlp13cg_md-0.5.1.tar.gz

# OntoServer install (development only)
Download the Docker Desktop

docker login quay.io 

user name: unimelbproject2023

password: 20232023di

docker-compose up -d

docker exec ontoserver /index.sh -v 20230328

# System Requirements (for delivery)
1. 8GB memory, at least
2. At least 10GB of storage space is required
3. Need Internet for the first time install everything.

# Running setup for deploy (development only)
serve -s dist
python main.py

# Setup for delivery (Video in Product page in confluence)
Run **Setup.bat**

Or using following steps:
1. Install Docker Desktop and change the container path
2. Go to 'src' directory
3. Using following cmd 'docker login quay.io' and then type user name and password. 
4. Using the following cmd 'docker-compose up -d'
5. Using the following cmd 'docker exec ontoserver /index.sh', if error, try multiply times. If 100% and then appear error, ignore it. 
6. Go to docker desktop and make sure the 'ontoserver' container is running. Paste the following to browser for testing 'http://ontoserver:8080/fhir/ValueSet/$expand?url=http://snomed.info/sct?fhir_vs=refset/32570071000036102&count=10&filter=Cough'. If there are words return, means install success. If it is not, back to step 5 and do it again(SNOMED CT is not very stable).
7. Running all of the container. Click the container call 'node-1' and then click the port '3000' to open in browser or 'https://localhost:3000'.

# TIPS
1. Replace the UIL.xlsx(In src/backend) with the new UIL and rename it as the same and then delete ONLY the container in Docker to update.
2. SNOMED CT update is very frequency. In order to update SNOMED CT, delete everything in Docker (containers, images and volumes) and then click Setup.bat (The same as setup for delivery).


# Goals
![ExpectedOutcomes.png](https://imgpile.com/images/hNyBe1.png)
The core functionality of the project is to allow users to upload CSV files, algorithmically map the raw data files (CSV) to a list of common indications, and host this functionality through a local interface. The customer wishes to implement the system in two modes. One model is for researchers to directly upload data and then download transformed data from the system. Another mode is that after the researchers upload the data, they modify the wrongly mapped data through the interface to improve the system algorithm. In order to ensure that only relevant researchers can use the system, user login and registration are required. But only a handful of researchers will use the system, so it requires no administrators.


## How to use the medical data classification function in other code
First, ensure that you have the required Python libraries installed:

`pip install pandas scikit-learn nltk rake_nltk numpy`

Usage:
Train the classifier using the training dataset:
`classifier, text_vectorizer = train_nb_classifier()`


├── src/backend    # backend code and mapping algorithm
    
├── src/dist     # frontend packaging code
    
├── src/frontend     # front end code for development
    
├── src/Docker-setup   # docker setup files
    
├── src/Docker-setup/Docker-Mysql    # docker setup file for Mysql

├── src/Docker-setup/Docker-ontoserver    # docker setup file for ontoserver

├── prototypes/low fidelity/     # low fidelity files (prototype screens)


`result = predict_medical_text(classifier, text_vectorizer, test_text)`

`print('Is the text medical-related? :', result)`
