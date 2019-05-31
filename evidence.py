'''
In this file a singleton is created for u, to use this u just need to declare "from evidence import *"
then call the contents_finder() method by test.contents_finder(). To see more detail example, please go to test.py
'''
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
import gc
import string
import unicodedata

global stemmer
stemmer = PorterStemmer()
global file_dict_path
file_dict_path = "dict"
global term_title_map
term_title_map = json.load(open("term_title_map.json", 'r'))

global title_doc_map
title_doc_map = json.load(open("title_doc_map.json", 'r'))
global nonstop
nonstop = stopwords.words('english')
term_freq = json.load(open("term_freq.json", 'r'))



# text prepprocessing
def helper(name):

    name = name.replace("-lrb-", '').replace('-rrb-', '')
    words = []
    name = name.translate(str.maketrans('', '', string.punctuation))
    # print(name)
    for word in nltk.word_tokenize(name):
        word = stemmer.stem(word)
        if word not in nonstop:
            word = word.lower()
            words.append(word)
    return words

class EvidenceFinder:

    # pre-process the text
    def preprocess(self, name:[]):
        tmp = {}
        # find title according to the rarest word
        for word in name:

            tmp[word] = tmp.setdefault(word, 0)
            try:
                tmp[word] = term_freq[word]
            except:
                continue
        tmp = sorted(tmp.items(), key=lambda item:item[1])
        # return the key according to the value
        return [item[0] for item in tmp]

    # find all potential doc
    def find_all(self, word: str):
        titles = set()
        try:
            titles.update(term_title_map[word])
        except:
            titles = None
        return titles

    def similarity(self, name_zip: str, title: str, marker: int):

        title = helper(title)
        if marker == 1:
            titles = list(zip(*[title[i:] for i in range(2)]))
        else:
            titles = title
        common = 0
        for item in name_zip:
            if item in titles:
                common += 1

        l1 = len(name_zip)
        l2 = len(titles)
        return l1 + l2 - 2*common

    # find the one which hs the highest similarity
    def find_top(self, name: str):
        sim = 100
        final_title = ''
        # remove stop word and stem
        origin_name = helper(name)
        # to find match titles
        tmp_name = self.preprocess(origin_name)
        if len(tmp_name) > 0:
            list_name = self.find_all(tmp_name[0])
        else:
            list_name = None
        marker = 0
        if list_name:
            titles = list(list_name)
            if len(origin_name) == 1:
                name_zip = list(origin_name)
                marker = 0
            else:
                name_zip = list(zip(*[origin_name[i:] for i in range(2)]))
                marker = 1
            for title in titles:
                tmp = self.similarity(name_zip, title, marker)
                if tmp == 0:
                    final_title = title
                    sim = tmp
                    break
                elif tmp < sim:
                    sim = tmp
                    final_title = title
        else:
            final_title = None
        return final_title, sim

    # return the relevent contents of a name entity
    def contents_finder(self, ner: str):
        # find the most similar title
        title, sim = self.find_top(ner)
        # get the contents
        if not title is None:
            contents = []
            info = title_doc_map[title]
            for i in range(0, len(info), 3):
                no = "%03d" % info[i]
                path = "wiki-pages-text/wiki-" + str(no) + ".txt"

                cur_file = open(path, 'br')
                cur_file.seek(info[i+1])
                contents.extend(str(cur_file.read(info[i+2] - info[i+1]), encoding='utf-8').splitlines())
                cur_file.close()
            return contents
        else:
            return None


    # # find the content according to file tile
    # def contents_finder(self, name_lineno: str):
    #     tmp =  name_lineno.split()
    #     title = tmp[0].lower().replace('_', ' ')
    #     title = " ".join(helper(unicodedata.normalize("NFD", title)))
    #     print(title)
    #     info = title_doc_map[title]
    #     print(info)
    #     for i in range(0, len(info), 3):
    #         no = "%03d" % info[i]
    #         path = "wiki-pages-text/wiki-" + str(no) + ".txt"
    #
    #         cur_file = open(path, 'br')
    #         cur_file.seek(info[i+1])
    #         contents = str(cur_file.read(info[i+2] - info[i+1]), encoding='utf-8').split("\n")
    #         cur_file.close()
    #         for content in contents:
    #             astr = content.split()
    #             if astr[0] == tmp[0] and astr[1] == tmp[1]:
    #                 return content
    #     return None

test = EvidenceFinder()


