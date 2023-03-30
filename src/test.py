import scispacy
import spacy
import time
print(time.time())
nlp = spacy.load("en_ner_bionlp13cg_md")
print(time.time())
doc = nlp("Urinary tract infection")

fmt_str = "{:<15}| {:<6}| {:<7}| {:<8}"
print(fmt_str.format("token", "pos", "label", "parent"))

for token in doc:
    print(fmt_str.format(token.text, token.pos_, token.ent_type_, token.head.text))

print(time.time())