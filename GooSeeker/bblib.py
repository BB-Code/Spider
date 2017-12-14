from urllib import request
from urllib.parse import quote
from lxml import etree

class Treater(object):
	def __init__(self):
		self.xslt = ''
	# 从文件读取xslt
	def getXSLTFromFile(self,xsltFilePath):
		file = open(xsltFilePath,'r',encoding='utf-8')
		try:
			self.xslt = file.read()
		finally:
			file.close()
	# 从字符串获得xslt
	def getXSLTFromString(self,xsltString):
		self.xslt = xsltString

	#通过GooSeeker API接口获得xslt
	def getXSLTFromAPI(self,APIKey,theme,middle=None,bname=None):
		apiurl = "http://www.gooseeker.com/api/getextractor?key="+ APIKey +"&theme="+quote(theme)
		if(middle):
			apiurl = apiurl+"&middle="+quote(middle)
		if(bname):
			apiurl = apiurl+"&bname="+quote(bname)
		apiconn = request.urlopen(apiurl)
		self.xslt = apiconn.read()
		
	#返回当前xslt
	def getXSLT(self):
		return self.xslt
	#提取方法，入参是一个HTML DOM对象，返回是提取结果
	def extract(self,html):
		xslt_root = etree.XML(self.xslt)
		tarnsfrom = etree.XSLT(xslt_root)
		result_tree = tarnsfrom(html)
		return result_tree

	#提取方法，入参是html源码，返回是提取结果
	def extractHTML(self,html):
		doc = etree.HTML(html)
		return self.extract(doc)
