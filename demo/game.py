import requests
import re
from  pymongo import MongoClient

def get_html(url):
    res = requests.get(url,timeout=30)
    res.encoding = 'utf-8'
    res.raise_for_status
    return res.text

def get_gameInfo(url):
    html=get_html(url)
    #print(html)
    numlist = re.findall(r'<div class=\\"num\\">(.*?)</div>',html)
    titlelist = re.findall(r'title=\\"(.*?)\\"', html)
    imglist = re.findall(r'<img src=\\"(.*?)\\"',html)
    timelist = re.findall(r'<div class=\\"time\\">(.*?)</div>',html)
    txtlist = re.findall(r'<div class=\\"txt\\">(.*?)</div>',html)
    for each1,each2,each3,each4,each5 in zip(numlist,titlelist,imglist,timelist,txtlist):
        num = each1
        title = each2
        img = each3
        time =each4
        txt = each5
        try:
            if num == '':
                num = '未知'
            else:
                data ={
                    'num':num,
                    'img':img,
                    'title':title,
                    'time':time,
                    'desc':txt
                }
                DBConnect(data)
            print('插入数据完成')
        except:
            print("ERROR")

def DBConnect(data):
    conn =MongoClient('127.0.0.1',27017)
    db = conn.GameDB
    table = db.game_info
    table.insert_one(data)

def main():
    # url = 'http://db2.gamersky.com/LabelJsonpAjax.aspx?jsondata={%22type%22%3A%22updatenodelabel%22%2C%22isCache%22%3Atrue%2C%22cacheTime%22%3A60%2C%22nodeId%22%3A%2220465%22%2C%22isNodeId%22%3A%22true%22%2C%22page%22%3A1}'
    # get_gameInfo(url)
    for i in range(118):
        url ='http://db2.gamersky.com/LabelJsonpAjax.aspx?jsondata={%22type%22%3A%22updatenodelabel%22%2C%22isCache%22%3Atrue%2C%22cacheTime%22%3A60%2C%22nodeId%22%3A%2220465%22%2C%22isNodeId%22%3A%22true%22%2C%22page%22%3A'+str(i)+'}'
        get_gameInfo(url)


if __name__ =='__main__':
    main()

