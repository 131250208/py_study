# -*- coding:utf-8 -*-
'''
Created on 2017年5月30日

@author: wycheng
'''
from lxml import html
import requests
import json
import re

class CrawlWeibo:
    
    # 获取指定博主的所有微博card的list
    def getWeibo(self,id,page):#id（字符串类型）：博主的用户id，page（整型）：微博翻页参数
        
        url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id+'&containerid=107603'+id+'&page='+str(page)
        response=requests.get(url)
        ob_json=json.loads(response.text)
        
        list_cards=ob_json['cards']
        return list_cards# 返回本页所有的cards
    
    # 返回某条微博的热门评论的list
    def getComments(self,id,page):# id（字符串类型）：某条微博的id，page（整型）：评论翻页参数
        url='https://m.weibo.cn/api/comments/show?id='+id+'&page='+str(page)
        response=requests.get(url)
        ob_json=json.loads(response.text)
        
        list_comments=ob_json['hot_data']
        return list_comments
    
    def printAllTopic(self,page):
        list_cards=self.getWeibo('1713926427',page)
        # 遍历当页所有微博，输出内容，并根据id查找输出热门评论
        for card in list_cards:
            if card['card_type']==9:# 过滤出微博，card_type=9的是微博card，card_type=11的是推荐有趣的人
                id=card['mblog']['id']
                text=card['mblog']['text']
                if re.search('___', text)!=None:# 用正则匹配，将博文有下划线的微博过滤出来，有下划线的是“话题微博”
                     print '***'
                     print u"### 话题: "+text+'\n'
                     
                     #根据微博id获取热门评论，并输出
                     list_comments=self.getComments(id, 1)# 热门评论只需要访问第一页
                     count_hotcomments=1
                     for comment in list_comments:
                         created_at=comment['created_at']# 发表日期时间
                         like_counts=comment['like_counts']# 点赞数
                         
                         text=comment['text']# 评论内容
                         tree=html.fromstring(text)
                         text=tree.xpath('string(.)')# 用string函数过滤掉多余标签
                         
                         name_user=comment['user']['screen_name']# 评论者的用户名
                         
                         source=comment['source']# 来源于哪个终端
                         if source=='':
                             source=u'未知'
                             
                         pic_url=''# 评论内容的图片
                         if 'pic' in comment:
                             pic_url=comment['pic']['url']
                        
                        # 输出评论数据
                         print str(count_hotcomments),': **',name_user,'**',u'  **发表于：**'+created_at,u'  **点赞：**'+str(like_counts)+u'  **来自：**'+source
                         print text+'\n'
                         count_hotcomments=count_hotcomments+1
                     print '***'
                     
#实例化爬虫类并调用成员方法进行输出                     
# crawl_weibo=CrawlWeibo()
# crawl_weibo.printAllTopic(2)
       