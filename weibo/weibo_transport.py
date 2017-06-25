# -*- coding:utf-8 -*-
'''
Created on 2017年6月25日

@author: wycheng
'''
from crawl import crawl_weibo
import upload_driver
from lxml import html
import requests

class WeiboTransportor:
    
    def getContent(self,card):# 获取该card下微博的内容
        mblog=card['mblog']
        count_img=0# 每条微博重新计数图片
        
#         if 'retweeted_status' in mblog: #过滤掉有转发的微博
#             return None
#         
        #过滤掉定位
        
        text= html.fromstring(mblog['text'])
        text=text.xpath('string(.)')#过滤正文中的多余标签
        
        url_img=''
        if 'pics' in mblog:#有图片的存储图片
            pics=mblog['pics']
            for pic in pics:
                url_img=pic['large']['url']
                ir = requests.get(url_img)
                if ir.status_code == 200:# 如果请求得到响应
                    count_img+=1# 给图片计数
                    open('../img/'+str(count_img)+'.jpg', 'wb').write(ir.content)# 保存在img文件夹下，发送也从这个文件夹下找
                print u'图片：'+url_img
        

        
        scheme=card['scheme']
        created_at=mblog['created_at']
        source=mblog['source']
        reposts_count=mblog['reposts_count']
        comments_count=mblog['comments_count']
        attitudes_count=mblog['attitudes_count']
        
        return text,count_img,scheme,created_at,source,reposts_count,comments_count,attitudes_count

#
uploader=upload_driver.Uploader()
uploader.login('15850782585', 'Weibo6981228.')

# for i in range(38):
#     page=38-i 
crawl_weibo=crawl_weibo.CrawlWeibo()
cards=crawl_weibo.getWeibo('2622535523',34)
len_cards=len(cards)

wbtrans=WeiboTransportor()
for j in range(len_cards):
    index=len_cards-1-j
    
    card=cards[index]
    if card['card_type']==9 and not 'retweeted_status' in card['mblog']:# 如果是一条微博的card
        # 获取这条微博的内容
        content_list=wbtrans.getContent(card)
        text,count_img,scheme,created_at,source,reposts_count,comments_count,attitudes_count=content_list
            
        #发送这条微博的内容到新账号
        text=created_at+u'  来自 '+source+'\n'+text+' \n'+u'转发 '+str(reposts_count)+u'  评论 '+str(comments_count)+u'  点赞 '+str(attitudes_count)
        #打印
        print text
        print '=============================='
        print '\n'
        
        path_list=[]# 图片地址list
        for i in range(count_img):
            path_list.append('C:\\Users\\15850\\Documents\\GitHub\\MyWorkspace\\py_study\\img\\'+str(i+1)+'.jpg')
        # 上传内容
        if count_img==0:
            uploader.upload_txt(text)
        elif count_img==1:
            uploader.upload_txt_img(text, path_list[0])
        else:
            uploader.upload_txt_multiImg(text,path_list)
            
        uploader.send()