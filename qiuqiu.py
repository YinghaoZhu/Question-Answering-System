# This file generate training csv according to trainset.json
import json
import unicodedata
global title_doc_map
ori_title_doc_map = json.load(open("ori_title_doc_map.json", 'r'))
import testset
from evidence import *
from spacyusage import ner

# find the content according to file tile
def contents_finder(title: str):
    title = unicodedata.normalize("NFD", title)
    info = ori_title_doc_map[title]

    no = "%03d" % info[0]
    path = "wiki-pages-text/wiki-" + str(no) + ".txt"

    cur_file = open(path, 'br')
    cur_file.seek(info[1])
    contents = str(cur_file.read(info[2] - info[1]), encoding='utf-8').split("\n")
    cur_file.close()
    return contents


def csv_generator():
    generator = testset.test_csv("train2.csv")
    train = json.load(open("train.json", 'r'))
    keys = list(train.keys())
    i = 0
    for key in keys:
        try:
            item = train[key]
            if item["label"] != "NOT ENOUGH INFO":
                for evidence in item["evidence"]:
                    contents = contents_finder(evidence[0])
                    for content in contents:
                        words = content.split()
                        if int(words[1]) == evidence[1]:
                            generator.write(item["claim"], " ".join(words[2:]), item["label"])
                        else:
                            generator.write(item["claim"], " ".join(words[2:]), "NOT ENOUGH INFO")
        except:
            cur_f = open("log.txt", 'a')
            cur_f.write(key+"\n")
            cur_f.close()
            continue
csv_generator()