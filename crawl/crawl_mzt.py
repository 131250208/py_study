# -*- coding:utf-8 -*-
'''
Created on 2017年6月30日

@author: wycheng
'''
from kit_mine.request_mine import requests_mine
from bs4 import BeautifulSoup
import time

class CrawlMZT:
    
    # 保存一组图片
    def saveGroup(self,url):
        # 打开链接先找到最大页码数
        soup=BeautifulSoup(requests_mine.get(url).text,'lxml')        
        page_max=soup.find('div',class_='pagenavi').find_all('span')[-2].get_text()
        page_max=int(page_max)
        
        a_list=soup.find('div',class_='main-tags').find_all('a')
        tag_list=[]
        for a in a_list:
            tag_list.append(a.get_text())
        
        # 遍历每一页的链接，爬取图片，并在数据库储存数据
        for page in range(1,page_max+1):
            url_p=url+'/'+str(page)
            soup_p=BeautifulSoup(requests_mine.get(url_p).text,'lxml')
            img_list=soup_p.find('div',class_='main-image').find_all('img')
            for img in img_list:
                print img['src']
        
        print u'相关专题：'
        print tag_list
    def saveMZT(self):
        url_mzt = 'http://www.mzitu.com/all/'
        
        response = requests_mine.get(url_mzt)
        html_txt = response.text
        soup=BeautifulSoup(html_txt,'lxml')
        
        a_list = soup.find('div',class_='all').find_all('a')
        count_mzt = 0
        for a in a_list:
            url_img = a['href']
            title=a.get_text()
            count_mzt  += 1
            
            print str(count_mzt) + ":" + title + " : " + url_img
        
        print u'一共爬取了：' + str(len(a_list))

crawl_mzt=CrawlMZT()
crawl_mzt.saveGroup('http://www.mzitu.com/26685')