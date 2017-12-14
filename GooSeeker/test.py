import os
from urllib import request
from lxml import etree
from bblib import Treater

url = 'http://www.gooseeker.com/cn/forum/7'
conn = request.urlopen(url)
doc = etree.HTML(conn.read())

bbsExtra = Treater()
bbsExtra.getXSLTFromAPI("5cfce8d19fd49387277941a4d56efab0","en_test") # 设置xslt抓取规则
result = bbsExtra.extract(doc)


current_path = os.getcwd()
file_path = current_path+'/result.xml'

open(file_path,'wb').write(result)

print(str(result).encode('gbk','ignore').decode('gbk'))