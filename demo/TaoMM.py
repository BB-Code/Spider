#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Created on 2016-03-25 00:59:45
# Project: taobaomm

from pyspider.libs.base_handler import *
import os

page_start = 1
page_end = 30
dir_path = '/var/py/mm'

class Handler(BaseHandler):
    crawl_config = {}

    def __init__(self):
        self.base_url = 'https://mm.taobao.com/json/request_top_list.htm?page='
        self.page_num = page_start
        self.total_num = page_end
        self.deal = Deal()

    def on_start(self):
        while self.page_num <= page_end:
            url = self.base_url + str(self.page_num)
            self.crawl(url,callback=self.index_page,validate_cert=False)
            self.page_num +=1

    def index_page(self,response):
        for each in response.doc('.lady-name').items():
            self.crawl(each.attr.href,callback=self.detail_page,fetch_type='js',validate_cert=False)


    def detail_page(self,response):
        domain = response.doc('.mm-p-domain-info li>span').text()
        if domain:
            page_url = 'https:' + domain
            self.crawl(page_url,callback=self.domain_page,validate_cert=False)

    def domain_page(self,response):
        name = response.doc('.mm-p-model-info-left-top dd > a').text()
        dir_path = self.deal.mkDir(name)
        resume = response.doc('.mm-aixiu-content').text()
        if dir_path:
            imgs = response.doc('.mm-aixiu-content img').items()
            count = 1
            self.deal.saveResume(resume,dir_path,name)
            for img in imgs:
                url = img.attr.src
                if url:
                    extension = self.deal.getExtension(url)
                    file_name = name + str(count)+'.'+extension
                    count +=1
                    self.crawl(img.attr.src,callback=self.save_img,
                               save={'dir_path':dir_path,'file_name':file_name},validate_cert=False)
    def save_img(self,response):
        content = response.content
        dir_path = response.save['dir_path']
        file_name = response.save['file_name']
        file_path = dir_path +'/'+ file_name
        self.deal.saveImg(content,file_path)


    
        
class Deal:
    def __init__(self):
        self.path = dir_path
        if not self.path.endswith('/'):
            self.path = self.path + '/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def mkDir(self,path):
        path = path.strip()
        dir_path = self.path+ path
        exists = os.path.exists(dir_path)
        if not exists:
            os.makedirs(dir_path)
            return dir_path
        else:
            return dir_path
        

    def saveImg(self,content,path):
        f = open(path,'wb')
        f.write(content)
        f.close()

    def saveResume(self,content,dir_path,name):
        file_name = dir_path + '/'+name +'.txt'
        f = open(file_name,'w+')
        f.write(content)

    def getExtension(self,url):
        extension = url.split('.')[-1]
        return extension    