import requests as req
from bs4 import BeautifulSoup as bs

def get_html(url):
    res = req.get(url,timeout=30)
    res.raise_for_status
    res.encoding = ('utf-8')
    return res.text

def get_contents(url):
    urls = []
    html = get_html(url)
    soup = bs(html,'html.parser')

    category_list = soup.find_all('div',class_='index_toplist mright mbottom')

    for cate in category_list:
        name = cate.find('div',class_='toptab').span.string
        with open('C:\\Users\\Administrator\\Desktop\\Spiderxiaoshuo.csv','w')as f:
            f.write("\n小说种类：{}\n".format(name))
        general_list = cate.find(style='display: block;')
        book_list = general_list.find_all('li')

        for book in book_list:
            link = "http://www.qu.la/" + book.a['href']
            title = book.a['title']
            urls.append(link)
        with open('C:\\Users\\Administrator\\Desktop\\Spiderxiaoshuo.csv','w+') as f:
            f.write("小说名：{:<} \t 小说地址：{:<} \n".format(title, link))
    print('记录完毕')
    return urls
    

if __name__ == "__main__":
    url ='http://www.qu.la/paihangbang/'
    get_contents(url)
    

            
