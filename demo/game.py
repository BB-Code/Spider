import requests
import re
from  pymongo import MongoClient
import csv
def get_html(url):
    res = requests.get(url,timeout=30)
    res.encoding = 'utf-8'
    res.raise_for_status
    return res.text

def get_gameInfo(url):
    info_list = []
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
                info_list.append([num,img,title,time,txt])
                return info_list
                # writer(info_list)
                # print('写入数据完成',info_list)
        except:
            print("ERROR")

def DBConnect(data):
    conn =MongoClient('127.0.0.1',27017)
    db = conn.GameDB
    table = db.game_info
    table.insert_one(data)

def writer(info_list):
    with open('C:\\Users\\Administrator\\Desktop\\test.csv','a+', newline='')as f:
        writer = csv.writer(f,lineterminator='\n')
        writer.writerow(['评分', '图片路径', '标题', '发布时间','简介'])
        for row in info_list:
            writer.writerow(row)
            print(row)
def main():
    # url = 'http://db2.gamersky.com/LabelJsonpAjax.aspx?jsondata={%22type%22%3A%22updatenodelabel%22%2C%22isCache%22%3Atrue%2C%22cacheTime%22%3A60%2C%22nodeId%22%3A%2220465%22%2C%22isNodeId%22%3A%22true%22%2C%22page%22%3A1}'
    # get_gameInfo(url)
    for i in range(1,118):
        url ='http://db2.gamersky.com/LabelJsonpAjax.aspx?jsondata={%22type%22%3A%22updatenodelabel%22%2C%22isCache%22%3Atrue%2C%22cacheTime%22%3A60%2C%22nodeId%22%3A%2220465%22%2C%22isNodeId%22%3A%22true%22%2C%22page%22%3A'+str(i)+'}'
        info_list=get_gameInfo(url)
        #print(info_list)
        writer(info_list)


if __name__ =='__main__':
    main()

