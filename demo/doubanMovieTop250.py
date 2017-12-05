import requests
from bs4 import BeautifulSoup
import re

def get_url(url):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
    res = requests.get(url,headers= headers)
    return res

def find_movies(res):
    movies = []
    soup = BeautifulSoup(res.text,'html.parser')
    targets = soup.find_all("div","hd")
    for each in targets:
        movies.append(each.a.span.text)

    ranks = []
    targets = soup.find_all("span",class_="rating_num")
    for each in targets:
        ranks.append('评分:%s' % each.text)

    messages = []
    targets = soup.find_all("div","bd")
    for each in targets:
        try:
            messages.append(each.p.text.split('\n')[1].strip() + each.p.text.split('\n')[2].strip())
        except:
            continue
        
    results =[]
    length = len(movies)
    for i in range(length):
        results.append(movies[i]+ranks[i]+messages[i]+'\n')
    return results


def find_page(res):
    soup = BeautifulSoup(res.text,'html.parser')
    page = soup.find("span",class_="next").previous_sibling.previous_sibling.text
    return int(page)



def main():
    server = "https://movie.douban.com/top250"
    res = get_url(server)
    page = find_page(res)

    result = []
    for i in range(page):
        url = server+'/?start='+str(25*i)
        res = get_url(url)
        result.extend(find_movies(res))

    with open("豆瓣电影Top250.txt","w",encoding="utf-8") as f:
        for each in result:
            f.write(each)

if __name__ == "__main__":
    main()
    











    
