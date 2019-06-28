# -*- coding: utf-8 -*
import requests #引入函式庫
from bs4 import BeautifulSoup
import re
import threading as thd
import time

def cur_time():
    localtime = time.asctime( time.localtime(time.time()) )
    print("現在時間為 :", localtime)
    
def fn():
    print(time.time())
    thd.Timer(10,fn).start()
    
def send_ifttt(title,url_send):   # 定義函式來向 IFTTT 發送 HTTP 要求
    topic_sharp = title.find('#')
    if topic_sharp != -1:
        global topic_send
        topic_send = title[:topic_sharp]+title[topic_sharp+1:]  
    else:
        topic_send = title
             
    url = ('https://maker.ifttt.com/trigger/line/with/' +
          'key/ckB0GpPvgCpuFl9Wv0D57J' +
          '?value1=' + topic_send +
          '&value3=' + url_send
          )
    r = requests.get(url)      # 送出 HTTP GET 並取得網站的回應資料
    if r.text[:5] == 'Congr':  # 回應的文字若以 Congr 開頭就表示成功了
        print('已傳送 (' +str(title)+') 到 Line')
    return r.text

def get_content():
    title_30=[]
    url_30=[]
    main_url = 'https://www.dcard.tw'
    url = 'https://www.dcard.tw/f/ncut?latest=true'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    dcard_title = soup.find_all('h3', re.compile('PostEntry_title_'))
    dcard_url = soup.find_all('a' ,attrs={"class":"PostEntry_root_V6g0rd"})
    print('Dcard 勤益版：')
    
    for text in dcard_title[:6]:
        title_30.append(text.getText())
    
    for text in dcard_url[:6]:
        url_30.append(main_url + text.get('href'))
        
    return title_30,url_30

def update(title,url,old_title,new_title):      
    if old_title == new_title:
        print("No Change")
    else:
        index = title.index(old_title)
        for i in reversed(range(index)):
            send_ifttt(title[i],url[i])
        old_title = new_title
            
    return old_title
    
    
if __name__ == "__main__":
    sleeptime = 30
    title=[]
    url=[]
    title,url = get_content()
    old_title = title[0]
    for i in reversed(range(len(title))):
        send_ifttt(title[i],url[i])
        
    while 1:
        title,url = get_content()
        new_title = title[0]
        cur_time()
        old_title = update(title,url,old_title,new_title)        
        time.sleep(sleeptime)

        
