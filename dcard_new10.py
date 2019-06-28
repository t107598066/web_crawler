# -*- coding: utf-8 -*
import requests #引入函式庫
from bs4 import BeautifulSoup
import re
import threading as thd
import time

topic_send=""
url_send=""

def fn():
    print(time.time())
    thd.Timer(10,fn).start()
    
def send_ifttt(v1,url_send):   # 定義函式來向 IFTTT 發送 HTTP 要求
    topic_sharp = v1.find('#')
    if topic_sharp != -1:
        global topic_send
        topic_send = v1[:topic_sharp]+v1[topic_sharp+1:]  
    else:
        topic_send = v1
             
    url = ('https://maker.ifttt.com/trigger/line/with/' +
          'key/ckB0GpPvgCpuFl9Wv0D57J' +
          '?value1=' + topic_send +
          '&value3=' + url_send
          )
    r = requests.get(url)      # 送出 HTTP GET 並取得網站的回應資料
    if r.text[:5] == 'Congr':  # 回應的文字若以 Congr 開頭就表示成功了
        print('已傳送 (' +str(v1)+') 到 Line')
    return r.text

topic=[]
dcar_durl=[]
main_url = 'https://www.dcard.tw'
url = 'https://www.dcard.tw/f'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')
dcard_title = soup.find_all('h3', re.compile('PostEntry_title_'))
dcard_url = soup.find_all('a' ,attrs={"class":"PostEntry_root_V6g0rd"})
print('Dcard 熱門前十文章標題：')
for index, item in enumerate(dcard_title[:10]):
    #print("{0:2d}. {1}".format(index + 1, item.text.strip()))
    b = item.text.strip()
    topic.append(b)
    
print(topic)
for u in dcard_url[:10]:
    print(main_url + u["href"])
    a = main_url + u["href"]
    dcar_durl.append(a)

for i in range (10):
    ret = send_ifttt(topic[i],dcar_durl[i]) #傳送 HTTP 請求到 IFTTT
    #print('IFTTT 的回應訊息：',ret)# 輸出 IFTTT 回應的文字
    
#data = {'標題': topic,'URL':dcardurl}
#info = pd.DataFrame(data)
#print(info)


#ret = send_ifttt(topic,dcardurl)  
#print('IFTTT 的回應訊息：',ret) 



