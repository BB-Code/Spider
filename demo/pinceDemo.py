import requests
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool
import csv 
import time
def get_page(url):
	headers ={'user-agent':'Mozillo/5.0'}
	res = requests.get(url,timeout=30,headers=headers)
	res.raise_for_status
	res.encoding = res.apparent_encoding
	return res.text
def get_content(html):
	info_list =[]
	titleP = re.compile('<a .*?class=\"f14\"><b>(.*?)</b></a>')
	styleP = re.compile('类型：.*?>(.*?)</a>',re.S)
	subjectP = re.compile('题材：.*?>(.*?)</a>',re.S)
	testTimeP = re.compile('<li class=\"li02\">.*?测试时间：(.*?)\n\t\t\t\t\t\t</li>',re.S)
	scoreP = re.compile('<span class=\"ff\">(.*?)</span><br />',re.S)
	awesomeP =re.compile('<span class=\"count noneornot\">(.*?)</span>.*?>给力</a>',re.S)
	forCardP = re.compile('<span class=\"count noneornot\">(.*?)</span>.*?>求卡</a>',re.S)
	throughP = re.compile('<span class=\"count noneornot\">(.*?)</span>.*?>路过</a>',re.S)
	flatP = re.compile('<span class=\"count noneornot\">(.*?)</span>.*?>乏味</a>',re.S)
	title = re.findall(titleP,html)
	style = re.findall(styleP,html)
	subject = re.findall(subjectP,html)
	testTime = re.findall(testTimeP,html)
	score = re.findall(scoreP,html)
	awesome = re.findall(awesomeP,html)
	forCard = re.findall(forCardP,html)
	through = re.findall(throughP,html)
	flat = re.findall(flatP,html)
	for title,style,subject,testTime,score,awesome,forCard,through,flat in zip(title,style,subject,testTime,score,awesome,forCard,through,flat):
		info_list.append([title,style,subject,testTime,score,awesome,forCard,through,flat])
	return info_list

def writer(data):
	with open('gamedata.csv','a+',newline='')as f:
		writer = csv.writer(f,lineterminator='\n')
		#writer.writerow(['标题', '类型', '题材', '测试时间','评分','给力','求卡','路过','乏味'])
		for row in data:
			writer.writerow(row)
			print(row)

def main(i):
	url='http://top.sina.com.cn/more.php?p='+str(i)
	print("当前的链接"+url)
	time.sleep(1)
	html=get_page(url)
	#print(html)
	info_list=get_content(html)
	writer(info_list)

if __name__=='__main__':
	pool = Pool()
	pool.map(main,[i for i in range(1,110)])

