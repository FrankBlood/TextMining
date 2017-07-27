# -*- coding:utf8 -*-

import json
import os
import sys

def test1():
    with open('new_json_data', 'r') as fp:
        for line in fp.readlines():
            json_data = json.loads(line.decode('utf8'))
            print json_data['weibo']
            break

def test2():
    num = 0
    topics = os.listdir('/home/irlab0/Research/DataSet/data_text/')
    for topic in topics:
        users = os.listdir('/home/irlab0/Research/DataSet/data_text/'+topic)
        num += len(users)
    print num

if __name__ == '__main__':
    test2()