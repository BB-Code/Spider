'''
爬取最新电影排行榜单
url：http://dianying.2345.com/top/
使用 requests --- bs4 线路
Python版本： 3.6
OS： Win7
'''
import requests 
from bs4 import BeautifulSoup as BS
from pymongo import MongoClient
'''
获取链接
'''
def get_html(url):
    try:
        res = requests.get(url,timeout=30)
        res.raise_for_status
        res.encoding = 'gbk'
        return res.text
    except:
        print("Error")


def get_content(url):
    html = get_html(url)
    soup = BS(html,'html.parser')
    movies_list = soup.find('ul',class_='picList')
    movies = movies_list.find_all('li')
    for each in movies:
        index = each.find('i',class_='iNum').text
        img_url = 'http:'+each.find('img')['src']
        name  = each.find('span',class_='sTit').a.text
        try:
            time = each.find('span',class_='sIntro').text
        except:
            time ="暂无上映时间"
        actor_list = each.find('p',class_='pActor')
        actors = ''
        for actor in actor_list.contents:
            actors = actors + actor.string + ' '
        intro = each.find('p',class_='pTxt pIntroShow').text
        datas ={
            "index":index,
            "name":name,
            "time":time,
            "actors":actors,
            "intro":intro,
            "img_url":img_url
        }
        Save_info(datas)
    print('导入数据库完成')


        #print("排名:{}\t 片名:{}\t{}\n{}\n{}\n\n".format(index,name,time,actors,intro))
        # with open('最新电影排行榜单.txt','a+',encoding='utf-8') as f:
        #     f.write("排名:{}\t 片名:{}\t{}\n{}\n{}\n\n".format(index,name,time,actors,intro))
        # with open('C:/Users/Administrator/Desktop/LearnSpider/img/'+name+'.png','wb+') as f:
        #     f.write(requests.get(img_url).content)  

def Save_info(datas):
    conn = MongoClient('localhost',27017)
    db = conn.moviesDB
    table = db.movies
    table.insert_one(datas)



def main():
    url='http://dianying.2345.com/top/'
    get_content(url)

if __name__=='__main__':
    main()
    
    
    
    