import requests
import re
from multiprocessing  import pool
import time,random
import csv
def get_url(url):
	proxies ={
		 "https": "http://60.169.221.128:24743",
  		 "https": "http://116.248.162.147:80"
	}
	headers ={'user-agent':'Mozilla/5.0','Host':'db.18183.com'}
	try:
		res = requests.get(url,timeout=30,headers=headers,proxies=proxies)
		res.raise_for_status
		res.encoding = res.apparent_encoding
		print(res.status_code)
		return res.text
	except:
		pass


def get_hero_url(html):
	pattern =re.compile('<div class="section hero-result-box.*?<ul class=\"mod-iconlist\">(.*?)</ul>',re.S)
	newHtml = re.findall(pattern,html)
	pattern2 = re.compile('<a href=\"(.*?)\">',re.S)
	urllist = re.findall(pattern2,str(newHtml))
	return urllist

def get_hero_content(hero_html):
	heroinfo = []
	pattern = re.compile('<h1>(.*?)</h1>',re.S)
	heroname = re.findall(pattern,str(hero_html))
	pattern2 = re.compile(
		'<dt>最大生命：(.*?)点</dt>.*?<dt>最大法力：(.*?)点</dt>.*?<dt>物理攻击：(.*?)点</dt>.*?<dt>法术攻击：(.*?)点</dt>'+
		'.*?<dt>物理防御：(.*?)点</dt>.*?<dt>物理减伤率：(.*?)</dt>.*?<dt>法术防御：(.*?)点</dt>.*?<dt>法术减伤率：(.*?)%</dt>'+
		'.*?<dt>移速：(.*?)点</dt>.*?<dt>物理护甲穿透：(.*?)点</dt>.*?<dt>法术护甲穿透：(.*?)点</dt>.*?<dt>攻速加成：(.*?)点</dt>'+
		'.*?<dt>暴击几率：(.*?)</dt>.*?<dt>暴击效果：(.*?)点</dt>.*? <dt>物理吸血：(.*?)点</dt>.*?<dt>法术吸血：(.*?)点</dt>'+
		'.*?<dt>冷却缩减：(.*?)点</dt>.*?<dt>攻击范围：(.*?) </dt>.*?<dt>韧性：(.*?)点</dt>.*?<dt>生命回复：(.*?)点</dt>'+
		'.*?<dt>法力回复：(.*?)点</dt>',re.S)
	hero_info = re.findall(pattern2,str(hero_html))
	for item,name in zip(hero_info,heroname):
		health=item[0]
		mana=item[1]
		attack_damage=item[2]
		ability_power=item[3]
		armor=item[4]
		armor_percent=item[5]
		magic_resist=item[6]
		magic_resist_percent=item[7]
		movement_speed=item[8]
		armor_penetration=item[9]
		magic_penetration=item[10]
		attack_speed=item[11]
		critical_strike_chance=item[12]
		critical_damage=item[13]
		life_steal=item[14]
		spell_vamp=item[15]
		cooldown_reduction=item[16]
		attack_range=item[17]
		tenacity=item[18]
		health_regen=item[19]
		mana_regen=item[20]
		heroinfo.append([name,health,mana,attack_damage,ability_power,armor,armor_percent,magic_resist,magic_resist_percent,movement_speed,armor_penetration,magic_penetration,attack_speed,critical_strike_chance,critical_damage,life_steal,spell_vamp,cooldown_reduction,attack_range,tenacity,health_regen,mana_regen])
	return heroinfo

def writer(data):
	with open('wzdata.csv','a+',newline='')as f:
		writer = csv.writer(f)
		writer.writerow(['英雄','最大生命','最大法力', '物理攻','法术攻击', '物理防御', '物理减伤率',' 法术防御','法术减伤率','移速','物理护甲穿透','法术护甲穿透','攻速加成','暴击几率','暴击效果','物理吸血','法术吸血','冷却缩减','攻击范围','韧性','生命回复','法力回复'])
		for row in data:
			writer.writerow(row)
			print(row)
def main():
	url ='http://db.18183.com/wzry/'
	html=get_url(url)
	urllist=get_hero_url(html)
	newurl="http://db.18183.com"
	for each in urllist:
		hero_html= get_url(newurl+each)
		time.sleep(random.random()*3)
		print("当前获取的链接："+newurl+each)
		heroinfo=get_hero_content(hero_html)
		writer(heroinfo)


if __name__=='__main__':
	main()
