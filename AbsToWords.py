# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 12:06:58 2019

@author: fengyichao
"""

#### 分词、去除标点符号、去除停用词

import re
import json
import nltk
from nltk.corpus import stopwords
import multiprocessing


def delPuncDigits(line):
    r1 = '[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~0123456789]+'
    filter_line = re.sub(r1, '', line).strip()
    return filter_line

def map_getWords(key_val_list):
    key = key_val_list[0]
    val = key_val_list[1]
    print("Get Words: " + key + "," + str(len(val)))
    words = []
    for title,abst in val:
        if abst:
            abst = delPuncDigits(abst)    ## 去除标点符号
            words.extend(nltk.word_tokenize(abst.lower()))   ## 分词
            words = [w for w in words if w not in stopwords.words("english")]
    return [key,words]

def getWords(abstracts):
    abs_word = {}
    abs_list = [[key,val] for key,val in sorted(abstracts.items())]
    pool = multiprocessing.Pool(processes=16)
    res = pool.map(map_getWords, abs_list)
    for key,val in res:
        abs_word[key] = val
    return abs_word

if __name__ == '__main__':
    
    abstracts = json.load(open('abstracts.json'))
    abs_word = getWords(abstracts)
    json.dump(abs_word, open('abs_word.json','w'))
    print("----------- Done: Get words.")
    
