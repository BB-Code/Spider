# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import json

headers = {'user-agent':'Mozilla/5.0'}

def get_img_url(url):
    res = requests.get(url,timeout=30,headers=headers)
    res.encoding = res.apparent_encoding
    res.raise_for_status
    return res.text

def get_html(id_list,url):
    res = requests.get(url,timeout=30,headers=headers)
    res.encoding = res.apparent_encoding
    res.raise_for_status
    list=json.loads(res.text)['data']['searchDOList']
    for i in list:
        id_list.append(i['userId'])
    return id_list

def get_mo_html():
    id_list = []
    url_list =[]
    url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
    id_url=get_html(id_list,url)
    #print(id_list)
    for each in id_list:
        girlurl = 'https://mm.taobao.com/self/album/open_album_list.htm?charset=utf-8&user_id='+ str(each)
        url_list.append(girlurl)
    #print(url_list[0])
    res = requests.get(url_list[0],timeout=30,headers=headers)
    res.encoding = res.apparent_encoding
    res.raise_for_status
    return res.text

def get_content():
    html = get_mo_html()
    img_json = []
    url_list = re.findall(r'<a class="mm-first" href=".*&album_id=(\d+).*" target="_blank">',html)

    #print(url_list)
    for each in url_list:
       	page = len(url_list)
       	for i in range(page):
	        url ='https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id=176817195&album_id='+str(each)+'&page='+str(i)
	        img_json.append(url)
	        for each  in img_json:
	        	img_json_item = get_img_url(each)
	        	print(img_json_item)
	        	img_dict=json.loads(img_json_item)
	    		print(type(img_dict))
	    		img_ll =img_dict['picList']
	    		for i in img_ll:
	    			img = 'https:'+i['picUrl']
	        		pic_id =i['picId']
	        		download_img(pic_id,img)
	    		print('下载完成')

def download_img(pic_id,img):
    with open(r'C:\\Users\\Administrator\\Desktop\\img\\'+pic_id+'.jpg','wb+') as f:
        f.write(requests.get(img).content)
        f.close()   
get_content()