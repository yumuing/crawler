# -*- coding: utf-8 -*
import sys
import time
import random

import requests
from lxml import html
import re
from pymongo import MongoClient
from fake_useragent import UserAgent

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# import _thread
def get_areas(str):
    print('开始')
    # 随机头信息
    headers = {
        'User-Agent': UserAgent().random
    }
    # 随机ip
    proxy = get_proxy().get("proxy")
    proxies = {
        'http:': 'http://{}'.format(proxy),
        'https:': 'https://{}'.format(proxy),
    }
    url = 'https://wh.fang.lianjia.com/loupan/' + str
    try:
        requests.packages.urllib3.disable_warnings()
        res = requests.get(url, headers=headers, proxies=proxies, verify=False)
        context = html.etree.HTML(res.text)
        # ul = context.xpath('//ul[@class="resblock-list-wrapper"]')  # 获取标签,按页遍历
        # for i in ul:
        #     li=i.xpath('.//li[@class="resblock-list post_ulog_exposure_scroll has-results"]')
        ul = context.xpath('//ul[@class="resblock-list-wrapper"]')  # 获取标签,按页遍历
        # 楼盘列表div[@class="resblock-list-contaner clearfix"]
        # /li[@class="resblock-list post_ulog_exposure_scroll has-results"]
        for i in ul:# 遍历每一个ul[@class="resblock-list-wrapper"下的每一个li标签
            li = i.xpath('.//li[@class="resblock-list post_ulog_exposure_scroll has-results"]')
            for y in li:
             try:
              con= y.xpath('.//div[@class="resblock-desc-wrapper"]')
              # 在楼盘列表div[@class="resblock-list-contaner clearfix"]
              # /li[@class="resblock-list post_ulog_exposure_scroll has-results"]/ul[@class="resblock-list-wrapper"]
              for a in con:#遍历con
                    dict = {}#字典，存放key,value
                    dict["area1"] = a.xpath(".//div[@class='resblock-location']/span[1]/text()")
                    dict["area1"] = "".join(dict["area1"])
                    # dict["detail_area"] = dict["detail_area"][:]
                    print(dict["area1"])#地区
                    dict["title"] =a.xpath(".//div[@class='resblock-name']/a/text()")
                    dict["title"]="".join(dict["title"])
                    # dict["title"] = dict["title"][:]
                    print(dict["title"])
                    dict["area"] =a.xpath(".//div[@class='resblock-location']/span[2]/text()")
                    dict["area"] = "".join(dict["area"])
                    # dict["detail_area"] = dict["detail_area"][:]
                    print(dict["area"])
                    dict["detail_place"] = a.xpath(".//div[@class='resblock-location']/a/text()")#
                    dict["detail_place"] = "".join(dict["detail_place"])
                    # dict["detail_place"] = dict["detail_place"][:]
                    print(dict["detail_place"])
                    dict["type"] = a.xpath(".//div[@class='resblock-name']/span[1]/text()")
                    dict["type"] = "".join(dict["type"])#为了连接转为字符串
                    print(dict["type"])

                    try:

                         dict['square'] = a.xpath('.//div[@class="resblock-area"]//span//text()')
                         dict['square'] = "".join(dict['square'])
                         dict['square'] = re.findall(r"\d+-\d+" + "㎡", dict['square'])#正则取值
                         dict['square'] = "".join(dict['square'])#以”“将列表数据拼接成字符串·

                         print( dict['square'])
                         dict['sum_Price'] = a.xpath('.//div[@class="resblock-price"]//div[@class="second"]//text()')
                         dict['sum_Price'] = "".join(dict['sum_Price'])
                         dict['sum_Price'] = re.findall(r"\d+\.?\d+" , dict['sum_Price'])
                         dict['sum_Price'] = "".join(dict['sum_Price'])
                         print( dict['sum_Price'])
                    except Exception as e:
                        dict['square'] = ""
                    dict['price'] = a.xpath('.//div[@class="resblock-price"]//div[@class="main-price"]//span[1]//text()')[0]

                    #价格待定的楼盘设置price为0
                    if dict['price']=='价格待定':
                        dict['price'] = 0

                        dict['sum_Price'] = 0
                    dict['price']=float( dict['price'])
                    if  dict['square'] == None:
                          dict['square'] = 0

                    list = []
                    list.append(dict)
                    client = MongoClient(host='localhost', port=27017)
                    db = client.get_database("lianjia2")
                    col = db.get_collection("loupan")
                    col.insert_many(list)
                    time.sleep(random.randint(1, 5))
             except Exception as e:
                print(res.text)
                print(url)
                print( 'ooops! connecting error, retrying.....')

        sleeptime = random.randint(30, 35)
        print("睡眠了%d秒" %sleeptime)
        time.sleep(sleeptime)
    except requests.exceptions.ProxyError as e:
        delete_proxy(proxy)

if __name__ == '__main__':
    # 遍历的页数
    for i in range(1, 48):
        print("正在爬取第%d页" % i)
        get_areas("pg" + str(i))
        print("任务完成")
    print("爬完")