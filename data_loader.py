#!/usr/bin/env python
# -*- coding:utf8 -*-
# 加载程序包
import os, sys
import json
import codecs
import jieba
import numpy as np
import pandas as pd

# 数据读取
class Data_Loader(object):

    def __init__(self, file_path='/home/irlab0/Research/DataSet/data_text/',
                 tag_file = './tmp/file_tag.xlsx',
                 tag_path = './tmp/tags/',
                 tag_features = './tmp/tag_features',
                 new_path='./tmp/json_data',
                 embedding_path='./tmp/cn_embedding/wordvecs.txt',
                 embedding_vcb_path='./tmp/cn_embedding/wordvecs.vcb'):

        self.file_path = file_path
        self.tag_file = tag_file
        self.tag_path = tag_path
        self.tag_features = tag_features
        self.new_path = new_path
        self.embedding_path = embedding_path
        self.embedding_vcb_path = embedding_vcb_path
        self.labels = ['cartoon', 'constellation', 'emotion', 'fashion',
                       'film', 'food', 'game', 'house', 'music', 'science',
                       'sports', 'travel', 'tv']
        print 'data loading...'

    def loader(self):
        data = []
        label_list = os.listdir(self.file_path)
        for label in label_list:
            user_list = os.listdir(self.file_path+label)
            for user in user_list:
                if os.path.exists(self.file_path+label+'/'+user+'/'+user+'.txt'):
                    data.append((label, user, self.file_path+label+'/'+user+'/'+user+'.txt'))
        print("The size of data is", len(data))
        return data

    def to_json(self, data):
        fw = open(self.new_path, 'a')
        for user in data:
            with codecs.open(user[-1], encoding='gbk') as fp:
                weibo = fp.read()
                # print weibo
                dict_data = {'label': user[0], 'user':user[1], 'weibo': weibo.encode('utf8')}
                # print weibo.read()
                # print dict_data
            json_data= json.dumps(dict_data)
            fw.write(json_data.encode('utf8')+'\n')
        fw.close()

    def get_embedding_matrix(self):
        print('Preparing embedding matrix...')

        vcb = []
        embeddings = []
        with codecs.open(self.embedding_vcb_path, encoding='utf8') as fp:
            for line in fp.readlines():
                vcb.append(line.strip())

        with codecs.open(self.embedding_path) as fp:
            for line in fp.readlines():
                embeddings.append(line.strip().split(','))

        embedding_matrix = {}

        for word, embedding in zip(vcb, embeddings):
            embedding_matrix[word] = np.array(embedding, float)

        print('num of word embeddings:', len(vcb))

        return embedding_matrix

    def get_tag(self):
        for label in self.labels:
            df = pd.read_excel(self.tag_file, sheetname=label)
            new_df = df[[u'用户兴趣类别', u'标签', u'用户ID(oid)']]
            print(new_df)
            new_df.to_csv('./tmp/tags/'+label+'.csv', encoding='utf8', index=False)

    def tag2feature(self):

        def get_json_data(line, tags):
            feature = [0] * len(tags)
            for word in line[u'标签'].strip().split(' '):
                feature[tags.index(word)] += 1
            json_data = json.dumps({"user":line[u'用户ID(oid)'],
                                    "label":line[u'用户兴趣类别'].encode('utf8'),
                                    "feature":feature})
            return json_data

        fw = open(self.tag_features, 'a')
        tags = []
        for label in self.labels:
            df = pd.read_csv(self.tag_path+label+'.csv', encoding='utf8')
            for tag in df[u'标签']:
                tags += tag.strip().split(' ')

        tags = list(set(tags))
        with open('./tmp/tags_text', 'a') as fww:
            for tag in tags:
                fww.write(tag.encode('utf8')+'\n')

        for label in self.labels:
            df = pd.read_csv(self.tag_path+label+'.csv', encoding='utf8')
            # print(df.head())
            # print(df.apply(len, axis=1))
            df['json_data'] = df.apply(lambda line: get_json_data(line, tags), axis=1)
            df['json_data'].apply(lambda x: fw.write(x+'\n'))

        fw.close()


# def test_feature():
#     data_loader = Data_Loader()
#     data_loader.tag2feature()

# def test_tag():
#     data_loader = Data_Loader()
#     data_loader.get_tag()

# def main():
#     data_loader = Data_Loader()
#     data = data_loader.loader()
#     data_loader.to_json(data)
#     # data_loader.get_embedding_matrix()

if __name__ == '__main__':
    data_loader = Data_Loader()
    data_loader.tag2feature()