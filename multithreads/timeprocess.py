#!/usr/bin/env python   
# -*- coding: UTF-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import jieba.posseg as pseg
import json


past=['之后','后面','以后','后','年后']
before=['之前','前面','以前','前','年前']
pass_word=['首','一首','一千年','一个','一支','一曲','一些','上','周末','点','早上','摇滚','下','午后','次元','几年','首来','首后','正在','中','清晨','起','首在','夜晚','夜夜']
time_dic={
    '五十年代':[1950,1959],
    '六十年代':[1960,1969],
    '七十年代':[1970,1979],
    '八十年代':[1980,1989],
    '九十年代':[1990,1999],
    '五十年代末':[1956,1959],
    '六十年代末':[1966,1969],
    '七十年代末':[1976,1979],
    '八十年代末':[1986,1989],
    '九十年代末':[1996,1999],
    '五十年代初':[1950,1955],
    '六十年代初':[1960,1965],
    '七十年代初':[1970,1975],
    '八十年代初':[1980,1985],
    '九十年代初':[1990,1995],
    '八十年代末九十年代初':[1986,1995],
    '七十年代末八十年代初':[1976,1985],
    '六十年代末七十年代初':[1966,1975],
    '80年代末90年代初':[1986,1995],
    '70年代末80年代初':[1976,1985],
    '60年代末70年代初':[1966,1975],
    '50年代':[1950,1959],
    '60年代':[1960,1969],
    '70年代':[1970,1979],
    '80年代':[1980,1989],
    '90年代':[1990,1999],
    '50年代初':[1950,1955],
    '60年代初':[1960,1965],
    '70年代初':[1970,1975],
    '80年代初':[1980,1985],
    '90年代初':[1990,1995],
    '50年代末':[1956,1959],
    '60年代末':[1966,1969],
    '70年代末':[1976,1979],
    '80年代末':[1986,1989],
    '90年代末':[1996,1999],
    '两千年':[2000,2000],
    '1几年':[2010,2017],
    '0几年':[2000,2010],
}

CN_NUM = {
u'零' : 0,
u'一' : 1,
u'二' : 2,
u'三' : 3,
u'四' : 4,
u'五' : 5,
u'六' : 6,
u'七' : 7,
u'八' : 8,
u'九' : 9,
u'两' : 2,
u'千' : 0,
}

def converter(string):
    length=len(string)
    number=''
    n=0
    
    for i in range(0,(length/3)):
        try:
            tmp=CN_NUM[string[n:n+3].decode('utf8')]
            number=number+str(tmp)
        except:
            number=number+str(string[n:n+3])
        n=n+3
    return number


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def jieba_pseg(line):
    words=pseg.cut(line)
    process_word=[]
    for word, flag in words:
        process_word.append([word,flag]) 
        
    return process_word


def print_result(line):
    tmp=''
    process_word=jieba_pseg(line)
    
    less=''
    higher=''
    
    for line in process_word:
        flag=line[1]
        word=line[0]
        if flag == 'm' or flag == 't' or flag == 'f' or flag== 'z':
            if word.encode('utf8') not in pass_word:
                if is_number(word.encode('utf8'))==True:
                    tmp=tmp+str(word)
                else:
                    try:
                        list_tmp=time_dic[word.encode('utf8')]
                        tmp=tmp+str(word.encode('utf8'))
#                         less=list_tmp[0]
#                         higher=list_tmp[1]
#                         break
                    except:
                        tmp=tmp+converter(word.encode('utf8'))
    
    
    if tmp!='':
        second_check= jieba_pseg(tmp.decode('utf8'))
        tmp=''
        for line in second_check:
            tmp=tmp+line[1]
        
        
        if tmp=='mm':
            if len(second_check[0][0])==2:
                if int(second_check[0][0])>20:
                    less='19'+second_check[0][0]
                    higher='19'+second_check[0][0]
                elif int(second_check[0][0])<20:
                    less='20'+second_check[0][0]
                    higher='20'+second_check[0][0]
            elif len(second_check[0][0])==4:
                less=second_check[0][0]
                higher=second_check[0][0]
            else:
                return 'None','None'
            
        elif tmp=='mtfmtf' :
                try:
                    tmp_dic=second_check[0][0].encode('utf8')+second_check[1][0].encode('utf8')+second_check[2][0].encode('utf8')+second_check[3][0].encode('utf8')+second_check[4][0].encode('utf8')+second_check[5][0].encode('utf8')
                    list_tmp=time_dic[tmp_dic]
                    less=list_tmp[0]
                    higher=list_tmp[1]
                except:
                    return 'None','None'
        

        elif tmp=='mtf' :
            try:
                tmp_dic=second_check[0][0].encode('utf8')+second_check[1][0].encode('utf8')+second_check[2][0].encode('utf8')
                list_tmp=time_dic[tmp_dic]
                less=list_tmp[0]
                higher=list_tmp[1]
            except:
                return 'None','None'

        elif tmp=='m': 
            try:
                list_tmp=time_dic[second_check[0][0].encode('utf8')]
                less=list_tmp[0]
                higher=list_tmp[1]
            except:
                if len(second_check[0][0])==2:
                    return 'None','None'
                elif len(second_check[0][0])==4:
                    less=second_check[0][0]
                    higher=second_check[0][0]
                else:
                    return 'None','None' 
            
        elif tmp=='mmz':
            if len(second_check[0][0])==2:
                if int(second_check[0][0])>20:
                    less='19'+second_check[0][0]
                    higher='19'+second_check[0][0]
                elif int(second_check[0][0])<20:
                    less='20'+second_check[0][0]
                    higher='20'+second_check[0][0]
            elif len(second_check[0][0])==4:
                less=second_check[0][0]
                higher=second_check[0][0]
            else:
                return 'None','None'

        elif tmp=='tt':
            try:
                test_word=second_check[0][0].encode('utf8')+second_check[1][0].encode('utf8')
                list_tmp=time_dic[word.encode('utf8')]
                less=list_tmp[0]
                higher=list_tmp[1]
            except Exception, e:
                return 'None','None'
                
        elif tmp=='mt':
            try:
                test_word=second_check[0][0].encode('utf8')+second_check[1][0].encode('utf8')
                list_tmp=time_dic[test_word]
                less=list_tmp[0]
                higher=list_tmp[1]
            except:
                if second_check[1][0].encode('utf8') in past:
                    if len(second_check[0][0])==2:
                        if int(second_check[0][0])>20:
                            less='19'+second_check[0][0]
                            higher=2018
                        elif int(second_check[0][0])<20:
                            less='20'+second_check[0][0]
                            higher=2018
                    elif len(second_check[0][0])==4:
                        less=second_check[0][0]
                        higher=2018
                    else:
                        return 'None','None'
                elif second_check[1][0].encode('utf8') in before:
                    if len(second_check[0][0])==2:
                        if int(second_check[0][0])>20:
                            less=1980
                            higher=int('19'+second_check[0][0])+1
                        elif int(second_check[0][0])<20:
                            less=1980
                            higher=int('20'+second_check[0][0])+1
                    elif len(second_check[0][0])==4:
                        less=1980
                        higher=int(second_check[0][0])+1
                    else:
                        return 'None','None'
        elif tmp=='mtz':
            try:
                test_word=second_check[0][0].encode('utf8')+second_check[1][0].encode('utf8')
                list_tmp=time_dic[test_word]
                less=list_tmp[0]
                higher=list_tmp[1]
            except:
                if second_check[1][0].encode('utf8') in past:
                    if len(second_check[0][0])==2:
                        if int(second_check[0][0])>20:
                            less='19'+second_check[0][0]
                            higher=2018
                        elif int(second_check[0][0])<20:
                            less='20'+second_check[0][0]
                            higher=2018
                    elif len(second_check[0][0])==4:
                        less=second_check[0][0]
                        higher=2018
                    else:
                        return 'None','None'
                elif second_check[1][0].encode('utf8') in before:
                    if len(second_check[0][0])==2:
                        if int(second_check[0][0])>20:
                            less=1980
                            higher=int('19'+second_check[0][0])+1
                        elif int(second_check[0][0])<20:
                            less=1980
                            higher=int('20'+second_check[0][0])+1
                    elif len(second_check[0][0])==4:
                        less=1980
                        higher=int(second_check[0][0])+1
                    else:
                        return 'None','None'
        elif tmp=='mmf':
            if second_check[2][0].encode('utf8') in past:
                if len(second_check[0][0])==2:
                    if int(second_check[0][0])>20:
                        less='19'+second_check[0][0]
                        higher=2018
                    elif int(second_check[0][0])<20:
                        less='20'+second_check[0][0]
                        higher=2018
                elif len(second_check[0][0])==4:
                    less=second_check[0][0]
                    higher=2018
                else:
                    return 'None','None'
            elif second_check[2][0].encode('utf8') in before:
                if len(second_check[0][0])==2:
                    if int(second_check[0][0])>20:
                        less=1980
                        higher=int('19'+second_check[0][0])
                    elif int(second_check[0][0])<20:
                        less=1980
                        higher=int('20'+second_check[0][0])
                elif len(second_check[0][0])==4:
                    less=1980
                    higher=int(second_check[0][0])
                else:
                    return 'None','None'
        elif tmp=='xm':
            try:
                test_word=second_check[0][0].encode('utf8')+second_check[1][0].encode('utf8')
                list_tmp=time_dic[test_word]
                less=list_tmp[0]
                higher=list_tmp[1]
            except:
                return 'None','None'
        elif tmp=='mfz':
            try:
                list_tmp=time_dic[second_check[0][0].encode('utf8')+second_check[1][0].encode('utf8')]
                less=list_tmp[0]
                higher=list_tmp[1]
            except:
                return 'None','None'
        elif tmp=='mf':
            try:
                list_tmp=time_dic[second_check[0][0].encode('utf8')+second_check[1][0].encode('utf8')]
                less=list_tmp[0]
                higher=list_tmp[1]
            except:
                if second_check[1][0].encode('utf8') in past:
                    if len(second_check[0][0])==2:
                        if int(second_check[0][0])>20:
                            less='19'+second_check[0][0]
                            higher=2018
                        elif int(second_check[0][0])<20:
                            less='20'+second_check[0][0]
                            higher=2018
                    elif len(second_check[0][0])==4:
                        less=second_check[0][0]
                        higher=2018
                    else:
                        return 'None','None'
                elif second_check[1][0].encode('utf8') in before:
                    if len(second_check[0][0])==2:
                        if int(second_check[0][0])>20:
                            less=1980
                            higher=int('19'+second_check[0][0])
                        elif int(second_check[0][0])<20:
                            less=1980
                            higher=int('20'+second_check[0][0])
                    elif len(second_check[0][0])==4:
                        less=1980
                        higher=int(second_check[0][0])+1
                    else:
                        return 'None','None'
                
        elif 'mfmf' in tmp:
                try:
                    list_tmp=time_dic[second_check[0][0].encode('utf8')+second_check[1][0].encode('utf8')+second_check[2][0].encode('utf8')+second_check[3][0].encode('utf8')]
                    less=list_tmp[0]
                    higher=list_tmp[1]
                except:
                    return 'None','None'
        else:
            return 'None','None'
        
    else:
        return less,higher

    return less,higher

def output_time(question):
    less,higher=print_result(question)
    if less=='':
        less='None'
    if higher=='':
        higher='None'
    tmp={
	'time':{
    		'time_lower':str(higher),
    		'time_higher':str(less),
		}
    }
    return tmp
