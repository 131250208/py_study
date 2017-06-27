# -*- coding:utf-8 -*-
'''
Created on 2017年6月27日

@author: wycheng
'''
import requests
from lxml import html
from selenium import webdriver

# 关注某用户的关注列表
def follow_followlist(uid,page):# uid：用户的id page；用户关注列表的翻页参数
    url='http://weibo.com/p/100505'+uid+'/follow'+'?page='+str(page)# 关注列表页
    driver=webdriver.Chrome()
    driver.get(url)
    print driver.page_source
#     response=requests.get(url)
#     tree=html.fromstring(response.text)
#     nodes=tree.xpath('//ul[@node-type="userListBox"]')[0]
#     for node in nodes:
#         print node.get_attribute('action-data')

follow_followlist('2622535523', 1)