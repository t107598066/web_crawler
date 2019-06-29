# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import requests
import random
import time
import re
import threading as thd
from urllib.parse import unquote,quote

def cur_time():
    localtime = time.asctime( time.localtime(time.time()) )
    print("現在時間為 :", localtime)
    
def fn():
    print(time.time())
    thd.Timer(10,fn).start()
    
def send_ifttt(title_send,url_send):   # 定義函式來向 IFTTT 發送 HTTP 要求    
    title_send_encode = quote(title_send) #編碼成url    
    url = ('https://maker.ifttt.com/trigger/line/with/' +
          'key/ckB0GpPvgCpuFl9Wv0D57J' +
          '?value1=' + title_send_encode +
          '&value3=' + url_send
          )
    r = requests.get(url)      # 送出 HTTP GET 並取得網站的回應資料
    if r.text[:5] == 'Congr':  # 回應的文字若以 Congr 開頭就表示成功了
        print('已傳送 ('+ title_send +') 到 Line')
    time.sleep(1)
    return r.text

def get_topic_url(flag):
    url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
    randomint = random.randint(0,7)
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
        'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6'
     ]
    req = Request(            
        url,
        data=None,
        headers={
            'User-Agent':user_agents[randomint],
            "Cookie": "over18=1"
        }
    )
    
    html = urlopen(req)
    soup = BeautifulSoup(html,'html.parser')
    
    title=[]
    url=[]
    matrix= [[],[]]
    ptt_title = soup.find_all('div',{"class":"title"})
    ptt_url = soup.find_all('a',attrs={'href':re.compile('^/bbs/Gossiping/M')})
        
    for content in ptt_title:         
        if content.getText().find("[公告] 八卦板板規") == -1:
            per_title = content.getText()          
            title.append(per_title) 
        else:
            break
        
    for content in ptt_url[:len(title)]:
        per_url = content.get('href') 
        url.append(per_url)        
                   
    for index,content in enumerate(title):    
        if content.find('(本文已被刪除)')==-1:
            matrix[0].append(content)
            matrix[1].append('https://www.ptt.cc' + url[index])
        else:
            matrix[0].append(content)
            matrix[1].append('')
            
    if len(matrix[0]) == 20:
        flag += 1 
    elif len(matrix[0]) < 20:
        flag = 0
            
    return flag,matrix
        
def update(old_matrix,new_matrix):
    old_len = len(old_matrix[0])
    new_len = len(new_matrix[0])
    start = old_len
    end = new_len
    
    if  new_len == old_len:
        print("No Change")
    elif new_len > old_len:        
        for i in range(start,end):     
            if new_matrix[0][i].find('(本文已被刪除)') == -1:          
                ret = send_ifttt(new_matrix[0][i],new_matrix[1][i])
                print('IFTTT sent:', ret) 
            else:
                pass  
            
        old_matrix = new_matrix        
        print(len(old_matrix[0]))        
    else:
        for i in range(new_len):
            ret = send_ifttt(new_matrix[0][i],new_matrix[1][i])
            print('IFTTT sent:', ret)   
        old_matrix = new_matrix
        
    return old_matrix
    
if __name__ == '__main__':
    
    sleeptime = 10
    ptt_new_title=[]
    ptt_new_url=[]
    ptt_old_title=[]
    ptt_old_url=[]        
    flag = 0     
    old_matrix = [[],[]]
    new_matrix = [[],[]]

    
    flag,old_matrix = get_topic_url(flag)
    for i in range(len(old_matrix[0])):
        if old_matrix[0][i].find('(本文已被刪除)') == -1: 
            ret = send_ifttt(old_matrix[0][i],old_matrix[1][i])
            print('IFTTT sent:', ret) 
            
        else:
            pass
    print(len(old_matrix[0]))
    while 1 :
        if flag < 2:
            flag,new_matrix = get_topic_url(flag)
            old_matrix = update(old_matrix,new_matrix)
            cur_time()
        else:
            cur_time()
            flag,new_matrix = get_topic_url(flag)
            print("No Change")
        time.sleep(sleeptime)