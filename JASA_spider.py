# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 20:06:21 2019

@author: fengyichao
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
import logging

def getVolHref(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    vol_list = soup.find('ul','list-of-issues').find_all('li','vol_li')
    dic = {}
    for vol in vol_list:
        dic[vol['id'][-4:]] = vol.a['href']
    return dic

def getIssueHref(vol_list):
    dic = {}
    for key in vol_list:
        print("{} {}".format(key,time.asctime(time.localtime(time.time()))))
        url = "https://www.tandfonline.com" + vol_list[key]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        li = []
        for issue in soup.find('li','vol_li active').ul.find_all('a'):
            li.append(issue['href'])
        dic[key] = li
    return dic

def HrefToAbstract(href):
    response = requests.get(href)
    soup = BeautifulSoup(response.text, 'lxml')
    soup_abstract = soup.find('div','abstractSection abstractInFull')
    if soup_abstract:
        soup_abstract_p = soup_abstract.find_all('p')
        if len(soup_abstract_p) > 0 :
            abstract = soup_abstract_p[len(soup_abstract_p)-1].string
        else:
            return None
    else:
        return None
    return abstract

def oneIssueAbstracts(issue):
    abs_list = []
    url = "https://www.tandfonline.com" + issue
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    soup_papers = soup.find('div','tocContent').find_all('table')
    for i,paper in enumerate(soup_papers):
        print("{}/{}".format(str(i+1),str(len(soup_papers))))
        title = paper.find('div','art_title linkable').string
        paper_url = ("https://www.tandfonline.com" + 
                     paper.find('div','art_title linkable').a['href'])
        try:
            abstract = HrefToAbstract(paper_url)
        except: 
            time.sleep(5)
            abstract = HrefToAbstract(paper_url)
        abs_list.append([title,abstract])
    return abs_list

if __name__ == '__main__':
    
#    vol_list_path = 'https://www.tandfonline.com/loi/uasa20'
#
#    print("----------- Begin: get volume list")
#    vol_list = getVolHref(vol_list_path)
#    json.dump(vol_list, open('vol_list.json','w'))
#    print("----------- Done: get volume list")
#
#    time.sleep(5)
#    print("----------- Begin: get issue list")
#    issue_list = getIssueHref(vol_list)
#    json.dump(issue_list, open('issue_list.json','w'))
#    print("----------- Done: get issue list")
   
    issue_list = json.load(open('issue_list.json'))
    print("----------- Begin: get all abstracts")
    years = list(issue_list.keys())
    years.sort()
    years = [x for x in years if x > '2015']
    for key in years:
        try:
            dic = {}
            dic[key] = []
            print("---{}: There are {} issues.---".format(key,len(issue_list[key])))
            for i,issue in enumerate(issue_list[key]):
                print("Issue {}/{}".format(str(i+1),(len(issue_list[key]))))
                dic[key].extend(oneIssueAbstracts(issue))
            json.dump(dic, open(os.path.join('Abstracts',key+'.json'),'w'))
        except Exception as e:
            logging.exception(e)
            with open('fail_years.txt','a') as f:
                f.write(key + '\n')
    print("----------- Done: get all abstracts")

    







