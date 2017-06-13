#!/usr/bin/env python   
# -*- coding: UTF-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from timeprocess import output_time
from genreprocess import output_genre
from query_preprocess import query_pre
import json
import threading
from time import ctime,sleep
import time
import Queue
import requests
from collections import Counter
from flask import Flask

  


def worker_time(line,q):
    return_string=output_time(line)
    q.put(return_string)

def worker_genre(line,q):
    return_string=output_genre(line)
    q.put(return_string)

def worker_name(line,q):
    line = line.lower()
    start_name = time.clock()

    github_url = 'http://101.200.159.42:9001/vinci/naturelang/v2/metasearch?query='+line
    r = requests.post(github_url)
    try:
        content_list=r.json()['content']
        interface_singer_list = []
        for i in range(len(content_list)):
            interface_singer_list.append(content_list[i]['singer'])
        
        singer_counts = Counter(interface_singer_list)
        top_three = singer_counts.most_common(20)      
        synonym_singer = ''
        singer = []
        tmp_check=''
        for word in top_three:
            tmp_word = word[0].encode('utf8')
            tmp_word = tmp_word.lower()

            if tmp_word in synonym:
                synonym_singer = synonym[tmp_word].replace('\n','')
            else:
                synonym_singer = 'None'

            if tmp_word in line:
                flag=0
                for tmp_check in singer:
                    if tmp_word in tmp_check:
                        flag=1
                    else:
                        pass

                if word[0].replace(' ', '_') in all_singers and flag==0:
                    if word[0].encode('utf8').lower() not in singer:
                        singer.append(word[0].encode('utf8').lower())
                        tmp_check = tmp_word
                    #break
            elif synonym_singer.encode('utf8') in line:
                if word[0].encode('utf8').lower() not in singer: 
                    singer.append(word[0].encode('utf8'))
         #singer = synonym_singer
                    #break

        if singer == []:
            singer = ['None']        
    
        tmp={'artist':singer}

        q.put(tmp)
        end_name= time.clock()    
        print "read: %f s" % (end_name - start_name)
    except:
        tmp={'artist':['None']}
        q.put(tmp)

def song_name(line,q):
    line = line.lower()
    start_name = time.clock()

    github_url = 'http://101.200.159.42:9001/vinci/naturelang/v2/metasearch?query='+line
    r = requests.post(github_url)
    try:
        content_list=r.json()['content']
        interface_singer_list = []
                
        for i in range(len(content_list)):
            interface_singer_list.append(content_list[i]['song'])
        
        singer_counts = Counter(interface_singer_list)
        top_three = singer_counts.most_common()      
        synonym_singer = ''
        song=''
        
        for word in top_three:
            if word[1] > 50:
                tmp_song_name = word[0].encode('utf8')
                if tmp_song_name.lower() in line:
                    song=tmp_song_name
                    break
            else:
                break

        if song == '':
            song = 'None'  

        tmp={'song':song}

        q.put(tmp)
        end_name= time.clock()    
        print "read: %f s" % (end_name - start_name)
    except:
        tmp={'song':'None'}
        q.put(tmp)

def worker_name_single(line,p):
    github_url='http://101.200.159.42:9001/vinci/naturelang/v2/getsemantic?query='+line
    r = requests.post(github_url)
    tmp_song='None'
    tmp_artist='None'
    try:
        tmp_artist=r.json()['content']['artist']
    except:
        pass
    try:
        tmp_song=r.json()['content']['song']
    except:
        pass
    
    if tmp_artist =='None' and tmp_song=='None':
        p.put(['None',1])
    else:
        tmp={
            'artist':tmp_artist,
            'song':tmp_song
        }
        p.put([tmp,0])



all_singers=[]
singer_file = open("/home/lulu/Desktop/vinci/svm/server/multithreads/data/xiami_singer.dic","r")
lines = singer_file.readlines()
for line in lines:
    all_singers.append(line.strip("\n"))
singer_file.close()


synonym = {}
tup_in_synonym = [] 
synonym_file = open("/home/lulu/Desktop/vinci/svm/server/multithreads/data/synonym.txt")
synonym_pair = synonym_file.readlines()
for line in synonym_pair:
    tup_in_synonym = line.split('\t')
    synonym[tup_in_synonym[0]] = tup_in_synonym[1]
synonym_file.close()


api=Flask(__name__)
@api.route('/text/<string:question>',methods=['GET'])

def test_f(question):

        question = query_pre(question)

        q = Queue.Queue()
        p = Queue.Queue()

        
        threads = []
        t1 = threading.Thread(target=worker_time(question, q))
        threads.append(t1)
        t2 = threading.Thread(target=worker_genre(question, q))
        threads.append(t2)
        t3 = threading.Thread(target=worker_name(question ,q))
        threads.append(t3)
        t5 = threading.Thread(target=song_name(question, q))
        threads.append(t5)
        t4 = threading.Thread(target=worker_name_single(question, p))
        threads.append(t4)



        for t in threads:
            t.setDaemon(True)
            t.start()
            t.join()


        test=p.get()


        if test[1]==1:

            result=[]
            while not q.empty():
                result.append(q.get())
                result_dic={}
                for line in result:
                    for word in line:
                        result_dic[word]=line[word]

            #process return data structure
            check_time_dic = {"time_higher": "None", "time_lower": "None"}
            res = {"code": 200, "data": {}, "msg": ""}
            data_dic = {}
            for line in result_dic:
                if result_dic[line] != ["None"] and result_dic[line] != "None" and result_dic[line] != check_time_dic:
                    data_dic[line] = result_dic[line]

            res["data"] = data_dic

            if res["data"] == {}:
                res.pop("data")
            
            if res["code"] != 200:
                res.pop("data")
                res["msg"] = "error"

            if res["msg"] == "":
                res.pop("msg")
            return json.dumps(res,ensure_ascii=False)
        elif test[1]==0:
            #process return data structure
            res = {"code": 200, "data": {}, "msg": ""}
            if test[0]["artist"] == "None":
                test[0].pop("artist")
            else:
                test[0]["artist"] = [test[0]["artist"]]
            
            if test[0]["song"] == "None":
                test[0].pop("song")

            data_dic = test[0]

            res["data"] = data_dic

            if res["data"] == {}:
                res.pop("data")
            
            if res["code"] != 200:
                res.pop("data")
                res["msg"] = "error"

            if res["msg"] == "":
                res.pop("msg")

            return json.dumps(res,ensure_ascii=False)
        

if __name__=='__main__':
    api.run(host='0.0.0.0', port=5200, debug=True, threaded=True)
