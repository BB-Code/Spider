import requests as req
from bs4 import BeautifulSoup as bs

def get_html(url):
    try:
        r = req.get(url,timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Error"

def print_result(url):
    html = get_html(url)
    soup = bs(html,'html.parser')
    match_list = soup.find_all('div',class_='matchmain bisai_qukuai')
    for match in match_list:
        time = match.find('div',class_='whenm').text.strip()
        teamname = match.find_all('span',class_='team_name')

        if teamname[0].string[0:3] == 'php':
            team1_name = "暂无队名"
        else:
            team1_name = teamname[0].string

        team1_support_level = match.find('span', class_='team_number_green').string

        team2_name = teamname[1].string
        team2_support_level = match.find('span',class_='team_number_red').string
        with open('data.csv','a+',encoding="utf-8") as f:
            contents = "比赛时间：{}，\n 队伍一：{}      胜率 {}\n 队伍二：{}      胜率 {} \n".format(time,team1_name,team1_support_level,team2_name,team2_support_level)
            f.write(contents)
            f.close()
    print('记录成功!')  

def main():
    url = 'http://dota2bocai.com/match'
    print_result(url)
    
    

if __name__ == '__main__':
    main()
