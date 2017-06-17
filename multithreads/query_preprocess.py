
# coding: utf-8

# In[1]:

#!/usr/bin/env python   

import sys, os
reload(sys)
sys.setdefaultencoding('UTF-8')


# In[2]:

import jieba
import json


# In[3]:

#首先读出歌手同义词词典中的歌手信息
singer_synonym_dict = {}
tup_in_dict = []
singer_synonym_file = open(os.path.dirname(sys.argv[0])+'/data/xiamifilters.prop')
for line in singer_synonym_file:
    tup_in_dict = line.split('=')
    singer_synonym_dict[tup_in_dict[0]] = tup_in_dict[1].replace('\n','')



# In[4]:

#将读取的歌手同义词信息存入 singer_custom_dict.txt
singer_custom_list = []
for i in singer_synonym_dict:
    singer_custom_list.append(i.replace('\n',''))
    singer_custom_list.append(singer_synonym_dict[i].replace('\n',''))

singer_custom_list = list(set(singer_custom_list))

# for word in singer_custom_list:
#     print json.dumps(word, ensure_ascii=False)



# In[5]:

singer_custom_dict = open(os.path.dirname(sys.argv[0])+'/data/singer_custom_dict.txt', 'w')
for word in singer_custom_list: 
    singer_custom_dict.write(word)
    singer_custom_dict.write('\n')
singer_custom_dict.close()


# In[6]:

jieba.load_userdict(os.path.dirname(sys.argv[0])+'/data/singer_custom_dict.txt')


# In[11]:
def query_pre(query):
    new_query = query
    segs = jieba.cut(query, cut_all=False)
      
    for seg in segs:
        if seg.encode('utf8') in singer_synonym_dict:
            new_query = new_query.replace(seg,singer_synonym_dict[seg.encode('utf8')])
            # print json.dumps(new_query,ensure_ascii=False)
    return new_query
