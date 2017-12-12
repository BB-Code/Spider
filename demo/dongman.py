#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-12-12 08:56:34
# Project: dongman

from pyspider.libs.base_handler import *
import re
import pymongo
class Handler(BaseHandler):
    crawl_config = {
    }

    client = pymongo.MongoClient('localhost')
    db =client['dongman']
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.hahadm.com/list', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.oper > a:last-child').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        next = response.doc('.pages > a:last-child ').attr.href
        self.crawl(next,callback= self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        name = response.doc('.fn').text()
        img = response.doc('.pic > a > img').attr('src')
        p_list = response.doc('.oh > p').text()
        style = re.search('类别：(.*?)首播：',p_list).group(1)
        pubdate = re.search('首播：(.*?)导演：',p_list).group(1)
        director = re.search('导演：(.*?) 原作：',p_list).group(1)
        original = re.search('原作：(.*?)编剧：',p_list).group(1)
        region = re.search('地区：(.*?) 发音：',p_list).group(1)
        desc = response.doc('.intro > p').text()[5:]
        return {
            "url": response.url,
            "name":name,
            "img":img,
            "style":style,
            "pubdate":pubdate,
            "pubdate":pubdate,
            "director":director,
            "original":original,
            "region":region,
            "desc":desc
        }
     
    def on_result(self,result):
        if result:
            self.save_to_mongodb(result)
            
    def save_to_mongodb(self,result):
        if self.db['dongman_info'].insert(result):
            print("保存数据成功！",result)
        
            