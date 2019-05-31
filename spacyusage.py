'''
        This file is used for generate dev and test csv according claim
        There are three steps.
        First, Name Entity Recognition and Post of Speech tag,
        Sencond, according NER and POS find potential article and contents
        Then, generate "Claim" and "Evidence" pair to feed neural network
'''

import spacy
import json
from evidence import *
from testset import *
class NER:

    def __init__(self):
        self.nlp1 = spacy.load('xx_ent_wiki_sm')
        self.nlp2 = spacy.load('en_core_web_sm')
        self.csv = test_csv("devset.csv")

    # NER recognition
    def get_ner(self, claim: str):
        ner = set()
        doc1 = self.nlp1(claim)
        flag = 0
        for ent in doc1.ents:
            ner.add(ent.text)

        doc2 = self.nlp2(claim)
        for i in range(1, len(doc2)):
            if doc2[i].pos_ == 'VERB':
                ner.add(doc2[i-1].text)
                break

        # remove redundency
        ner2 = ner.copy()
        for item in ner2:
            for tmp in ner2:
                if tmp != item and item in tmp and item in ner:
                    ner.remove(item)
                    continue
        return list(ner)

    # poteintial title based on NER
    def finder(self, claim: str):
        tmp = []
        for ner in self.get_ner(claim):
            title, sim = test.find_top(ner)
            if title:
                tmp.append(title)
        return tmp

    # return the relevant contents of a NER
    def get_contents(self, claim: str, key: str):
        tmp = []
        for ner in self.get_ner(claim):
            contents = test.contents_finder(ner)
            if contents:
                tmp.extend(contents)
        self.csv.write(claim, tmp, key)

    # generate test set from json file
    def test_generator(self, path: str):
        i = 0
        testset = json.load(open(path, 'r'))
        keys = list(testset.keys())
        for key in keys[:8000]:
            i += 1
            print(i)
            if testset[key]["label"] == "NOT ENOUGH INFO":
                claim = testset[key]["claim"]
                claim = claim.translate(str.maketrans('', '', string.punctuation))
                self.get_contents(claim, key)
        self.csv.close()



# sigleton
ner = NER()
