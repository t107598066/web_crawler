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
    url = 'https://www.ptt.cc/bbs/sex/index.html'
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
    ptt_title = soup.find_all('div',{"class":"title"})
    ptt_url = soup.find_all('a',attrs={'href':re.compile('^/bbs/sex/M')})
        
    for content in ptt_title:  
        if content.getText().find("[公告] 西斯板規") == -1:
            if content.getText().find("(本文已被刪除)") == -1: 
                per_title = content.getText()          
                title.append(per_title)                
            else:
                pass                
        else:
            break
        
    for index,link in enumerate(ptt_url[:len(title)]): 
        if title[index].find("(本文已被刪除)") != -1: 
            pass
        else:
            url.append('https://www.ptt.cc' + link.get('href'))        
        
    ptt_title_len = len(title)
    
    if ptt_title_len == 20:
        flag += 1 
    elif ptt_title_len < 20:
        flag = 0
         
    return flag,ptt_title_len,title,url        

def index_title(ptt_cout,ptt_title):
    try:
        ptt_cout = ptt_title.index(ptt_title[ptt_cout])
    except ValueError:
        ptt_cout-=1
        ptt_cout = index_title(ptt_cout,ptt_title)
        
    return ptt_cout
            
def update(ptt_cout,ptt_title_len,ptt_title,ptt_url):    
    
    if ptt_title_len == ptt_cout:
        print("No Change")
    elif ptt_title_len > ptt_cout:
        #找old title 是否存在             
        ptt_cout = index_title(ptt_cout,ptt_title)
        
        for i in range(ptt_cout,ptt_title_len):                
            ret = send_ifttt(ptt_title[i],ptt_url[i])
            print('IFTTT sent:', ret) 
        ptt_cout = ptt_title_len
        print(ptt_cout)
    else :
        ptt_cout = 0
        ptt_cout = update(ptt_cout,ptt_title_len,ptt_title,ptt_url)
    
    if ptt_cout == 20:
        ptt_cout = 0
    
    return ptt_cout
    
    
if __name__ == '__main__':
    
    sleeptime = 10
    ptt_title=[]
    ptt_url=[]
    ptt_cout=0
    ptt_title_len=0
    flag = 0     

    while 1:
        flag,ptt_title_len,ptt_title,ptt_url = get_topic_url(flag)
        if flag < 2:
            ptt_cout = update(ptt_cout,ptt_title_len,ptt_title,ptt_url)
            cur_time()
            
        else:
            cur_time()
            print("No Change")
        time.sleep(sleeptime)

