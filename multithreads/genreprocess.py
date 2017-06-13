#!/usr/bin/env python   
# -*- coding: UTF-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import json
import operator
from tgrocery import Grocery 

#loading training file and make training data
f = file("/home/lulu/Desktop/vinci/svm/server/multithreads/data/addition.json")
s = json.load(f)
f.close

train_src = []
tup_in_train_src = ()

for i in range(len(s)):
    for word in s[i]['tags']:
        tup_in_train_src = (s[i]['playlistname'], word.replace('-','').lower())
        train_src.append(tup_in_train_src)

#train model
grocery_artist = Grocery('artist')
grocery_artist.train(train_src)
grocery_artist.save()

#load trained model
new_grocery_artist = Grocery('artist')
new_grocery_artist.load()


#loading training file and make training data
f = file("/home/lulu/Desktop/vinci/svm/server/multithreads/data/localRecommend.json")
s = json.load(f)
f.close

train_src = []
tup_in_train_src = ()

for i in range(len(s)):
    for word in s[i]['tags']:
        tup_in_train_src = (s[i]['playlistname'], word.replace('-','').lower())
        train_src.append(tup_in_train_src)


#train model
grocery = Grocery('query_grocery')
grocery.train(train_src)
grocery.save()

new_grocery = Grocery('query_grocery')
new_grocery.load()



def check(word):
    own_test_case_result=new_grocery.predict(word)

    own_test_all_dic=[]
    for line in own_test_case_result.dec_values:
        own_test_all_dic.append([line,own_test_case_result.dec_values[line]])
    
    own_test_all_dic=sorted(own_test_all_dic,key=operator.itemgetter(1), reverse=True)
    
    tmp=[]
    for line in own_test_all_dic:
        if line[1]>=0.2:
            tmp.append(line)
    
    result=[]
    count=0
    if tmp!=[]:
        tmp_value=tmp[0][1]
        for line in tmp:
            if 2*line[1]>tmp_value:
                    result.append(str(line[0]))
        if len(result)!=0:
            return ' '.join(result)
        elif len(result)==0:
            return 'None'
    else:
        return 'None'

def check_artist(word):
    own_test_case_result=new_grocery_artist.predict(word)

    own_test_all_dic=[]
    for line in own_test_case_result.dec_values:
        own_test_all_dic.append([line,own_test_case_result.dec_values[line]])
    
    own_test_all_dic=sorted(own_test_all_dic,key=operator.itemgetter(1), reverse=True)
    
    tmp=[]
    for line in own_test_all_dic:
        if line[1]>=0:
            tmp.append(line)
    
    result=[]
    count=0
    if tmp!=[]:
        tmp_value=tmp[0][1]
        for line in tmp:
            if 2*line[1]>tmp_value:
                    result.append(str(line[0]))
        if len(result)!=0:
            return ' '.join(result)
        elif len(result)!=0:
            return 'None'
    else:
        return 'None'



def output_genre(question):
    string=check(question)
    add_string=check_artist(question)
    
    
    if string is None and add_string is None:
        tmp={'genre':'None'}

    elif string is None and add_string is not None:
        tmp={}
        tmp_split=add_string.split(' ')
        tmp={'genre':tmp_split}

    elif string is not None and add_string is None:
        tmp={}
        tmp_split=string.split(' ')
        tmp={'genre':tmp_split}

    elif string is not None and add_string is not None:
        tmp={}
        tmp_split=(string+' '+add_string).split(' ')
        if 'None' in tmp_split:
            tmp_split.remove('None')
        tmp={'genre':tmp_split}

    return tmp
