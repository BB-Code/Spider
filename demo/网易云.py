
import requests
import re
import pymysql
from multiprocessing import Pool
import time
def get_page(url):
	headers = {'user-agent':'Mozille/5.0'}
	res = requests.get(url,timeout=30,headers=headers)
	res.raise_for_status
	res.encoding = res.apparent_encoding
	print(res.status_code)
	return res.text

def get_content(html):
	info_list = []
	num_list =[]
	#print(html)
	parrent = re.compile(r'<span class=\"nb\">(.*?)</span>',re.S)
	listen_num_list= re.findall(parrent,html)
	parrent2 = re.compile(r'<a title=\"(.*?)\".*?class="msk"></a>',re.S)
	title_list= re.findall(parrent2,html)
	parrent3 = re.compile(r'<a.*?class=\"nm nm-icn f-thide s-fc3\">(.*?)</a>',re.S)
	athor_list= re.findall(parrent3,html)
	for listen_num in listen_num_list:
		if '万' in listen_num:
			listen_num = listen_num.replace('万','0000')
			num_list.append(listen_num)
		else:
			listen_num = listen_num
			num_list.append(listen_num)
	for title,athor,num in zip(title_list,athor_list,num_list):
		info_list.append([title,athor,num])
	return info_list

	
	
def save_to_mysql(info_list):
	#UnicodeEncodeError：'latin-1' codec can't encode characters in position 0-1: ordinal not in range(256) Scrapy
	conn = pymysql.connect(host='127.0.0.1',user='root',passwd='123',port=3306,db='wymuisc',charset="utf8")
	cursor=conn.cursor()
	count =0
	for info in info_list:
		title =info[0]
		author = info[1]
		listen_num = info[2]
		insert_sql = "INSERT INTO wyinfo(title,author,listen_num) VALUES(%s,%s,%s)"
		data_info = (title, author, listen_num)
		cursor.execute(insert_sql,data_info)
		count+=1
		conn.commit()
		print("完成"+str(count)+"条插入!")
	cursor.close()
	conn.close()

def main(i):
	url = 'http://music.163.com/discover/playlist/?offset='+str(i)
	print("第"+str(i)+"条url")
	time.sleep(1)
	html=get_page(url)
	info_list=get_content(html)
	save_to_mysql(info_list)
	

if __name__=='__main__':
	pool =Pool()
	pool.map(main,[i*35 for i in range(0,38)])
