import requests as req
from bs4 import BeautifulSoup as bs
import time

def get_html(url):
    try:
        r = req.get(url,timeout=30)
        r.raise_for_status()
        r.encoding ='utf-8'
        return r.text
    except:
        return "Error"

def get_content(url):
    comments = []
    html = get_html(url)
    soup = bs(html,'html.parser')
    liTags = soup.find_all('li',attrs={'class':' j_thread_list clearfix'})
    for li in liTags:
        comment = {}
        try:
            comment['title'] = li.find('a',attrs={'class':'j_th_tit'}).text.strip()
            comment['link'] = "http://tieba.baidu.com/" + li.find('a',attrs={'class':'j_th_tit'})['href']
            comment['name'] = li.find('span',attrs={'class':'tb_icon_author'}).text.strip()
            comment['time'] = li.find('span',attrs={'class':'is_show_create_time'}).text.strip()
            comment['replyNum'] = li.find('span',attrs={'class':'threadlist_rep_num center_text'}).text.strip()
            comments.append(comment)
        except:
            print('Error')
    return comments        

def OutFile(dict):
    with open('tieba.txt','a+') as f:
        for comment in dict:
            f.write('标题: {} \t 链接:{} \t 发帖人:{} \t 发帖时间:{} \t 回复数量: {} \n'.format(
                comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']))
            print('当前页面爬取完成')


def main(base_url,deep):
    url_list =[]
    for i in range(0,deep):
        url_list.append(base_url + "&pn" + str(50*i))
    print('所有的网页已经下载到本地！ 开始筛选信息。。。。')

    for url in url_list:
        content = get_content(url)
        OutFile(content)
    print('所有的信息都已经保存完毕！')

base_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'
deep = 5

if __name__ == '__main__':
    main(base_url, deep)
