import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
from multiprocessing import Pool
def get_page_url(url):
    try:
        headers = {'user-agent':'mozille/5.0'}
        res = requests.get(url,timeout=30,headers=headers)
        res.encoding = res.apparent_encoding
        if res.status_code == 200:
            return res.text
        else:
            return None
    except RequestException:
        return None

def get_content(html):
    try:
        soup = BeautifulSoup(html,'html.parser')
        if soup != None:
            title_list = soup.select("dl dt")
            for item in title_list:
                title = item.a.string
                url = 'http://www.jb51.net'+item.a['href']
                date = item.span.string
                yield{
                    'title':title,
                    'url':url,
                    'date':date[3:]
                }
    except TypeError:
        return None

def save_info_to_Mongo(content):
    conn = MongoClient('127.0.0.1',27017)
    db = conn['python']
    table = db['articles_info']
    table.insert_one(content)
    
        

def main():
    for i in range(1,181):
        url ='http://www.jb51.net/list/list_97_'+str(i)+'.htm'
        html = get_page_url(url)
        info = get_content(html)
        if info !=None:
            for item in info:
                save_info_to_Mongo(item)
                print('插入数据成功！',item['title'])

if __name__ == '__main__':
    main()
    
    