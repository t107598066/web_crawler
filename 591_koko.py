# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import hashlib
from urllib.request import urlopen,Request
import requests
import random
import time

sleeptime = 5
url = 'https://rent.591.com.tw/?kind=0&fbclid=IwAR3mgqo9pBTygtCTgN24bg7RcpuvLiJiC3SMDe6w47cSZ2-W0PKU7AkYxOQ&sex=0&region=1&section=3,5,8,1,12&rentprice=8000,14000&pattern=0&area=7,10&option=washer&other=tragoods,balcony_1&hasimg=1&not_cover=1'
def getHash(url):
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
            'User-Agent':user_agents[randomint]
        }
    )
        
    html = urlopen(req)
    soup = BeautifulSoup(html,'html.parser')
    content = soup.find_all('a' ,attrs={"target":"_blank"})
    content_str=""
    first_item = True
    for text in content:
        if text.parent.name == 'h3':
            if first_item:
                new_href = text['href']
                new_title = text.getText()
                first_item = False
            content_str +=  text.getText()
    print(new_title, new_href)
    return hashlib.sha224(content_str.encode('utf-8')).hexdigest(), new_title, new_href

current_hash, new_title, new_href = getHash(url)
old_title = new_title
def send_ifttt(new_title,new_href):   # 定義函式來向 IFTTT 發送 HTTP 要求   
    url = ('https://maker.ifttt.com/trigger/line/with/' +
          'key/ckB0GpPvgCpuFl9Wv0D57J' +
          '?value1=' + new_title +
          '&value3=' + new_href
          )
    r = requests.get(url)      # 送出 HTTP GET 並取得網站的回應資料
    if r.text[:5] == 'Congr':  # 回應的文字若以 Congr 開頭就表示成功了
        print('已傳送 (' +str(new_title)+') 到 Line')
    return r.text

first=True
while 1:
    newhash, new_title, new_href = getHash(url)
       
    if old_title == new_title:    
        print("Not Changed")        
    else:       
        ret = send_ifttt(new_title,new_href)
        print('IFTTT sent:', ret)
        print(old_title,new_title)
        old_title = new_title
        current_hash = newhash
        
        
    time.sleep(sleeptime)




