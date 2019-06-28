# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import requests
import random
import time
import http.cookiejar
import re
import threading as thd
import urllib.request  

def cur_time():
    localtime = time.asctime( time.localtime(time.time()) )
    print("現在時間為 :", localtime)
    
def fn():
    print(time.time())
    thd.Timer(10,fn).start()
    
def send_ifttt(title_send,url_send):   # 定義函式來向 IFTTT 發送 HTTP 要求

    url = ('https://maker.ifttt.com/trigger/line/with/' +
          'key/ckB0GpPvgCpuFl9Wv0D57J' +
          '?value1=' + title_send +
          '&value3=' + url_send
          )
    r = requests.get(url)      # 送出 HTTP GET 並取得網站的回應資料
    if r.text[:5] == 'Congr':  # 回應的文字若以 Congr 開頭就表示成功了
        print('已傳送 (' +str(title_send)+') 到 Line')
    return r.text

def get_topic_url():
    url = 'https://rent.591.com.tw/?kind=0&fbclid=IwAR3mgqo9pBTygtCTgN24bg7RcpuvLiJiC3SMDe6w47cSZ2-W0PKU7AkYxOQ&sex=0&region=1&section=3,5,8,1,12&rentprice=8000,14000&pattern=0&area=7,10&option=washer&other=tragoods,balcony_1&hasimg=1&not_cover=1'
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
        }
    )
    
    html = urlopen(req)
    soup = BeautifulSoup(html,'html.parser')
    
    title=[]
    url=[]
    content = soup.find_all('a' ,attrs={"target":"_blank"})
        
    for text in content:
        if text.parent.name == 'h3':
            title.append(text.getText())
            url.append(text.get('href'))
                                                         
    return title,url        

def update(title,url,old_title,new_title):      
    if old_title == new_title:
        print("No Change")
    else:
        index = title.index(old_title)
        for i in reversed(range(index)):
            send_ifttt(title[i],url[i])
        old_title = new_title
            
    return old_title
        
if __name__ == '__main__':    
    sleeptime = 30
    title=[]
    url=[]   
    
    title,url = get_topic_url()
    old_title = title[0]
    cur_time()
    for i in reversed(range(len(title))):
        send_ifttt(title[i],url[i])

    while 1:
        title,url = get_topic_url()
        new_title = title[0]
        cur_time()
        old_title = update(title,url,old_title,new_title)        
        time.sleep(sleeptime)

