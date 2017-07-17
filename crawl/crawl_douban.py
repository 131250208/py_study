# -*- coding:utf-8 -*-
'''
Created on 2017年7月16日

@author: wycheng
'''
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()# chrome浏览器驱动
driver.implicitly_wait(10)# 设置隐性等待时间，等待页面加载完成才会进行下一步，最多等待10秒
driver.set_window_size(1920, 1080)# 用phantomjs必须有这行
wait = WebDriverWait(driver,10)
global count_href
count_href = 0

def getHref(page_index):
    global count_href
    url_rank = 'https://movie.douban.com/annual2016/?source=navigation#' + str(page_index)
    driver.get(url_rank)
    a_list = driver.find_elements_by_xpath('//a[contains(@href,"https://movie.douban.com/subject/")]')
    
    num = 0
    for a in a_list:
        num += 1
        print str(num) + ':' + a.get_attribute('href')
        count_href += 1
    
    print 'total:' + str(num)
def getHref_all():
    url_start = 'https://movie.douban.com/annual2016/?source=navigation#0'
    driver.get(url_start)
    div_list = driver.find_elements_by_xpath('//div[contains(@style,"transform:")]/div')
    pages_num = len(div_list)
    
    index = 1
    while index <= pages_num - 1 :
        getHref(index)
        time.sleep(3)
        index += 4
        
# getHref_all()
# print count_href

driver = webdriver.PhantomJS()# chrome浏览器驱动
driver.implicitly_wait(10)# 设置隐性等待时间，等待页面加载完成才会进行下一步，最多等待10秒
driver.set_window_size(1920, 1080)# 用phantomjs必须有这行
wait = WebDriverWait(driver,10)

driver.get('https://movie.douban.com/annual2016/?source=navigation#0')