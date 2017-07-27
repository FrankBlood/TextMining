#!/usr/bin/env python
# -*- coding:utf8 -*-
# 加载程序包
import os, sys
import json
import codecs
import jieba
import numpy as np
from data_loader import Data_Loader

class Pre_Process(object):

    def __init__(self, file_path = './tmp/json_data',
                 seg_path = './tmp/new_json_data',
                 stopwords_path = './tmp/stopwords',
                 weibo_vecs = './tmp/weibo_vecs'):

        self.file_path = file_path
        self.seg_path = seg_path
        self.stopwords_path = stopwords_path
        self.weibo_vecs = weibo_vecs
        print("pre processing...")

    def seg(self, text):
        seg_list = jieba.cut(text, cut_all=False)
        # print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
        return " ".join(seg_list)

    def seg_remove(self, stopwords):
        fw = open(self.seg_path, 'a')
        with codecs.open(self.file_path, encoding='utf8') as fp:
            for line in fp.readlines():
                try:
                    json_data = json.loads(line, encoding='utf8')
                    weibo = self.seg(json_data['weibo'])
                    new_weibo = []
                    for word in weibo.strip().split():
                        if word not in stopwords:
                            new_weibo.append(word)
                    new_weibo = " ".join(new_weibo)
                    json_data['weibo'] = new_weibo
                    # print json_data['weibo']
                    json_data = json.dumps(json_data)
                    fw.write(json_data+'\n')
                except:
                    pass
        fw.close()

    def get_stopwords(self):
        stopwords = []
        with codecs.open(self.stopwords_path, encoding='utf8') as fp:
            for word in fp.readlines():
                stopwords.append(word.strip())
        return stopwords

    def save_word2vec(self, embedding_matrix):
        fw = open(self.weibo_vecs, 'a')
        with codecs.open(self.seg_path) as fp:
            for line in fp.readlines():
                json_data = json.loads(line, encoding='utf8')
                weibo = json_data['weibo']
                weibo = weibo.strip().split()
                weibo_embedding = np.zeros(64)
                num = 0
                for word in weibo:
                    try:
                        weibo_embedding += embedding_matrix[word]
                        num += 1
                    except:
                        pass
                weibo_embedding = weibo_embedding / num
                fw.write(json.dumps({"weibo_vec":list(weibo_embedding),
                                     "user":json_data["user"],
                                     "label":json_data["label"]}) + '\n')

def get_seg_remove():
    pre_process = Pre_Process()
    stopwords = pre_process.get_stopwords()
    pre_process.seg_remove(stopwords)

def get_weibo_vecs():
    data_loader = Data_Loader()
    embedding_matrix = data_loader.get_embedding_matrix()

    pre_process = Pre_Process()
    pre_process.save_word2vec(embedding_matrix)

if __name__ == '__main__':
    # get_seg_remove()
    get_weibo_vecs()