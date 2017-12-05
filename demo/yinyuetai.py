import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

def get_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.61 Safari/537.36"}
    res = requests.get(url,timeout=30,headers=headers)
    res.raise_for_status
    res.coding = 'utf-8'
    return res.text

def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html,'html.parser')
    music = soup.find('ul',class_='area_three area_list')
    music_list = music.find_all('li',class_='vitem J_li_toggle_date ')
    for each in music_list:
        top_num = each.find('div',class_='top_num').text
        img_url = each.find('img')['src']
        mvname = each.find('a',class_='mvname').text
        special = each.find('a',class_='special').text
        time = each.find('p',class_='c9').text
        desc_score = each.find('div',class_='score_box').h3.text
        data={
            'top_num':top_num,
            'img_url':img_url,
            'mvname':mvname,
            'special':special,
            'time':time,
            'desc_score':desc_score
        }
        #DB(data)
        download_img(img_url,special)
    print('导入数据库完成')
        
def DB(data):
    conn = MongoClient('localhost',27017)
    db = conn.music
    table = db.music_top
    table.insert_one(data)

def download_img(img_url,special):
    with open('C:/Users/Administrator/Desktop/LearnSpider/music_img/'+special+'.jpg','wb+') as f:
        f.write(requests.get(img_url).content)
        f.close()
    print('下载图片完成')

def main():
    url='http://vchart.yinyuetai.com/vchart/trends?area=ML'
    get_content(url)

if __name__=='__main__':
    main()
