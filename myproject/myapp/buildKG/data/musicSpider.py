# -*- coding: utf-8 -*-
import json
import urllib3
from bs4 import BeautifulSoup

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # 改变标准输出的默认编码

# BeautifulSoup4将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象,
# 打开网页 获取网页内容
def url_open(url):
    userAgent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    http = urllib3.PoolManager(timeout=2)
    response = http.request('get', url, headers={'User_Agent': userAgent})
    html = response.data
    return html

# 与音乐有关的名次的列表
def musicList(filename):
    data = []
    fr = open(filename, 'rb')
    lines = fr.readlines()
    for line in lines:
       data.append(line.decode().strip('\n'))
    fr.close()
    return data
"""
def filter(text):
    text = value_node[i].get_text()
    text = text.replace('\n', '')
    text = text.replace(u'\uc774', u'')
    text = text.replace(u'\xa0', u'')
    text = text.replace(u'\ubc29', u'')
    text = text.replace(u'\xff', u'')
    text = text.replace(u'\xdf', u'')
    text = text.replace(u'\ubcf4', u'')
    text = text.replace(u'\ud669', u'')
    text = text.replace(u'\ubc15', u'')
    text = text.replace(u'\uc0e4', u'')
    text = text.replace(u'\ucd5c', u'')
    text = text.replace(u'\uc815', u'')
    text = text.replace(u'\uc5d1', u'')
    return text
"""



if __name__ == '__main__':
   musicItems = musicList('music.txt')
   musicItems = list(set(musicItems))   # 去重
   result_data = []
   for item in musicItems:
       url = "https://baike.baidu.com/item/"
       url = url + item
       bs = BeautifulSoup(url_open(url), features="html.parser")

       name_data = []
       value_data = []
       name_node = bs.find_all('dt', class_="basicInfo-item name")

       for i in range(len(name_node)):
           name_data.append(name_node[i].get_text().replace('    ', ''))

       value_node = bs.find_all('dd', class_="basicInfo-item value")

       for i in range(len(value_node)):
           text = value_node[i].get_text()
           text = text.replace('\n', ' ')
           text = text.strip()
           value_data.append(text)

       infor = dict(zip(name_data, value_data))   # 两个列表结合成字典形式

       # infor = json.dumps(infor, ensure_ascii=False)    # 字典转json 没必要
       if str(infor) != '{}':
           result_data.append(infor)

       print("数据爬取中……")
   print(result_data)
   fw = open('data.json', 'w')
   result_data = json.dumps(result_data, ensure_ascii=False)
   fw.write(result_data.encode("gbk", 'ignore').decode("gbk", "ignore"))   # bug
   fw.close()
   print('爬取结束……')
   """
     for item in musicItems:
       url = "https://baike.baidu.com/item/"
       url = url + 'item'
       bs = BeautifulSoup(url_open(url), features="html.parser")

       name_data = []
       value_data = []
       name_node = bs.find_all('dt', class_="basicInfo-item name")

       for i in range(len(name_node)):
           name_data.append(name_node[i].get_text().replace('    ', ''))

       value_node = bs.find_all('dd', class_="basicInfo-item value")

       for i in range(len(value_node)):
           value_data.append(value_node[i].get_text().replace('\n', ''))

       print(name_data)
       print(value_data)

       infor = dict(zip(name_data, value_data))
       print(infor)
   """


   """
   # 获取所有的a标签，并遍历打印a标签中的href的值
   print('=================href')
   for item in bs.find_all("a"):
       print(item.get("href"))
   print('================a')
    # 获取所有的a标签，并遍历打印a标签的文本值
   for item in bs.find_all("a"):
       print(item.get_text())

   """

   # print(data)