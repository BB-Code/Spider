#-*-coding:utf-8-*-
import requests
import re
from multiprocessing import Pool 

headers = {'user-agent':'mozille/5.0'}
def get_html(url):
	res = requests.get(url,timeout=30,headers=headers)
	res.encoding = res.apparent_encoding
	res.raise_for_status
	print(res.status_code)
	return res.text

def get_content(html):
	pattern = re.compile('<div class="pic">.*?<img src="(.*?)".*?</div>',re.S)
	info = re.findall(pattern,str(html))
	return info
def main(i):
	url = 'http://www.meizitu.com/a/more_'+str(i)+'.html'
	print('第'+str(i)+'页')
	html=get_html(url)
	img_url=get_content(html)
	for each in img_url:
		download(each)
		print("下载完成",each)

def download(img):
    with open('C:/Users/Administrator/Desktop/images/'+img[-22:-9].replace('/','')+'.jpg','wb+') as f:
        f.write(requests.get(img,headers=headers).content)
        f.close()

if __name__=='__main__':
	#main()
	pool = Pool()
	pool.map(main,[i for i in range(1,73)])
