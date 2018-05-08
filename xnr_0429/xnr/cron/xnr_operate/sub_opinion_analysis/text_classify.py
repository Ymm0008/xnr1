# -*- coding: utf-8 -*-

import os
import csv
import scws
import time
import re
import datetime
from datetime import datetime
from datetime import date
import heapq
import math
from config import *
import json
from duplicate import duplicate

class TopkHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []
 
    def Push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0][0]
            if elem[0] > topk_small:
                heapq.heapreplace(self.data, elem)
 
    def TopK(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in xrange(len(self.data))])]

def get_text_net(word, weibo_text,word_weight,max_n,min_n):

    c = dict()
    weight = dict()
    for i in range(0,len(weibo_text)):
        c[str(i)] = 0
        w_list = []
        for w in word:
            k1,k2 = w.split('_')
            c[str(i)] = c[str(i)] + weibo_text[i].count(str(k1))*word_weight[str(w)] + weibo_text[i].count(str(k2))*word_weight[str(w)]
            if w not in w_list:
                w_list.append(str(w))
        weight[str(i)] = float(len(w_list))/float(len(word))#c[str(k)]*(float(len(w_list))/float(len(word)))

    r_weibo = TopkHeap(max_n)
    for k,v in weight.iteritems():
        r_weibo.Push((v,k))#分类

    data = r_weibo.TopK()
    
    f_weibo = TopkHeap(min_n)
    for i in range(0,len(data)):
        k = data[i][1]
        f_weibo.Push((c[k],k))#排序

    data = f_weibo.TopK()
    text_list = []
    for i in range(0,len(data)):
        text = weibo_text[int(data[i][1])]
        text_list.append(text)
    
    return text_list

def get_count(word,text):

    count = 0
    for w in word:
        k1,k2 = w.split('_')
        if k1 in str(text):
            count = count + 1
        if k2 in str(text):
            count = count + 1

    return float(count)/float(len(word)*2)

def get_title(words,word_weight):#子话题名称

    word_dict = dict()
    for i in range(0,len(words)):
        k1,k2 = words[i].split('_')
        if word_dict.has_key(str(k1)):
            word_dict[str(k1)] = word_dict[str(k1)] + word_weight[words[i]]
        else:
            word_dict[str(k1)] = word_weight[words[i]]
        if word_dict.has_key(str(k2)):
            word_dict[str(k2)] = word_dict[str(k2)] + word_weight[words[i]]
        else:
            word_dict[str(k2)] = word_weight[words[i]]
    
    f_weibo = TopkHeap(5)
    for k,v in word_dict.iteritems():
        f_weibo.Push((v,k))#排序

    data = f_weibo.TopK()
    title = []
    for i in range(0,len(data)):
        word = data[i][1]#.decode('utf-8')
        title.append(word)
    return title    

def text_net(word_result,word_weight,weibo):#提取代表性微博_词网

    #进行文本去重
    text_list = []
    for i in range(0,len(weibo)):
        row = dict()
        row['_id'] = i
        row['title'] = ''
        row['content'] = weibo[i].decode('utf-8')
        text_list.append(row)

    results = duplicate(text_list)
    new_weibo = []
    for item in results:
        if not item['duplicate']:
            index = item['_id']
            new_weibo.append(weibo[index])

    max_n = int(len(new_weibo)*0.5) + 1
    min_n = len(new_weibo)/len(word_result.keys()) + 1
    #以下是提取每一类的代表性文本
    text_total = dict()
    opinion_name = dict()
    start = time.time()
    title = dict()
    dur_time = dict()
    for k,v in word_result.iteritems():
        text_list = get_text_net(v,new_weibo,word_weight,max_n,min_n)
        name = get_title(v,word_weight)#提取子话题名称
        opinion_name[k] = '&'.join(name)
        text_total[k] = text_list

    return text_total,opinion_name  

if __name__ == '__main__':
    #text_net('0522')#博鳌论坛
    text_net('maoming')#复旦投毒
