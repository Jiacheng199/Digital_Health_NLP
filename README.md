# Digital Health
#### DI-RedBack
# Project Overview
The project aims to set up and customise a tool and design a platform that will allow a human-in-the-loop to manually review the mapping results (between short free-text strings provided by clinical practitioners and SNOMED CT),
make corrections, and feed these back to re-train the system. This tool will be deployed using Docker inside an existing virtual machine..

# Background
Analysis of clinical documentation is critical for many digital health projects but extracting information from free-text clinical notes can be difficult. Typically, the rationale for prescribing a particular medication – the reason for prescription – is commonly provided by clinical practitioners in short free-text strings. We are interested in normalising those short strings by mapping them onto a knowledge base of canonical clinical terms, known as SNOMED CT (https://www.snomed.org/).
When a patient sees a doctor, the doctor records the patient's symptoms. However, doctors will abbreviate or modify it for the convenience of recording according to personal habits. The description of the symptoms that led to these symptoms is not part of the Universal Indication List. This makes it difficult to count and analyze symptoms. Therefore, it is necessary to turn the original file into a Universal Indication List.

# Running Enriovemnt
pip install nltk pymysql bcrypt jwt torch scipy
pip install spacy
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_bionlp13cg_md-0.5.1.tar.gz

# OntoServer install
Download the Docker Desktop

docker login quay.io 

user name: unimelbproject2023

password: 20232023di

docker-compose up -d

docker exec ontoserver /index.sh -v 20230328

# Running setup 
serve -s dist

python main.py

# Goals
![ExpectedOutcomes.png](https://imgpile.com/images/hNyBe1.png)
The core functionality of the project is to allow users to upload CSV files, algorithmically map the raw data files (CSV) to a list of common indications, and host this functionality through a local interface. The customer wishes to implement the system in two modes. One model is for researchers to directly upload data and then download transformed data from the system. Another mode is that after the researchers upload the data, they modify the wrongly mapped data through the interface to improve the system algorithm. In order to ensure that only relevant researchers can use the system, user login and registration are required. But only a handful of researchers will use the system, so it requires no administrators.

# Branching
## Quick Legend
|Instance|Branch|Description|
|:--:|:--:|:--:|
|Stable|main|Accepts merges from Sprint1-3|
|Working|sprint1|Always branch off Stable|
|Sprint2|sprint2|Always branch off Stable|
|Sprint3|sprint3|Always branch off Stable|

# Repository explanation

├── docs/                    # Documentation files

├── src/                       # src code

├── src/backend    # backend code and mapping algorithm
    
├── src/dist     # frontend packaging code
    
├── src/frontend     # front end code for development
    
├── src/Docker-setup   # docker setup files
    
├── src/Docker-setup/Docker-Mysql    # docker setup file for Mysql

├── src/Docker-setup/Docker-ontoserver    # docker setup file for ontoserver

├── prototypes/low fidelity/     # low fidelity files (prototype screens)

├── prototypes/high fidelity/     # high fidelity files (FIGMA source filesn)

├── ui/                        # All the images created for the prototypes

├── data samples/      

└── README.md
