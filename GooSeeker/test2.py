import os
import time
from lxml import etree
from selenium import webdriver

from bblib import Treater

#驱动火狐
driver = webdriver.Firefox()
# 访问并读取网页内容
url = "https://www.amazon.cn/b/ref=s9_acss_bw_ct_refTest_ct_1_h?_encoding=UTF8&node=658810051&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=merchandised-search-5&pf_rd_r=WJANDTHE4NFAYRR4P95K&pf_rd_t=101&pf_rd_p=289436412&pf_rd_i=658414051"
#开始加载
driver.get(url)
#等待2秒，更据动态网页加载耗时自定义
time.sleep(2)
# 获取网页内容
content = driver.page_source.encode('utf-8')
# 获取docment
doc = etree.HTML(content)

# 引用提取器
bbsExtra = Treater()   
bbsExtra.getXSLTFromAPI("31d24931e043e2d5364d03b8ff9cc77e", "亚马逊图书_test") # 设置xslt抓取规则
result = bbsExtra.extract(doc)   # 调用extract方法提取所需内容

# 当前目录
current_path = os.getcwd()
file_path = current_path + "/result2.xml"

# 保存结果
open(file_path,"wb").write(result)

# 打印出结果
print(str(result).encode('gbk','ignore').decode('gbk'))
driver.close()