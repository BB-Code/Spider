# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random
def get_html(url):
    headers ={"user-agent":"Mozilla/5.0"}
    result = requests.get(url,timeout=30,headers=headers)
    result.encoding = 'utf-8'
    result.raise_for_status
    return result.text

def get_img(url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html.parser')
    imglist = soup.find_all("img",class_="picact")
    for each in imglist:
        img = each['src']
        print(img)
        download(img)
def download(img):
    with open('C:/Users/Administrator/Desktop/images/'+img[-9:],'wb+') as f:
        f.write(requests.get(img).content)
        print("下载完成")

def main():
    #url2 ='http://www.gamersky.com/ent/201712/985787.shtml'
    #get_img(url2)
    for i in range(7):
        url='http://www.gamersky.com/ent/201711/984282_'+str(i)+'.shtml'
        get_img(url)

if __name__ =="__main__":
    main()