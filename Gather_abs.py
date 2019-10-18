# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 11:49:11 2019

@author: fengyichao
"""

import os
import json

Abs_dir = os.listdir("Abstracts")

dic = {}
print("------------ Begin: gather abstracts")
for filename in sorted(Abs_dir):
    print(filename)
    data = json.load(open(os.path.join("Abstracts",filename)))
    dic[list(data.keys())[0]] = data[list(data.keys())[0]]
json.dump(dic, open('abstracts.json','w'))
print("------------ Done: gather abstracts")
