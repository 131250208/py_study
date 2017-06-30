# -*- coding:utf-8 -*-
'''
Created on 2017年6月25日
此类实现了微博搬家，即批量发微博和关注
@author: wycheng
'''
from crawl import crawl_weibo
from weibo import weibo_op_driver
from lxml import html
import requests

def getContent(card):# 获取该card下微博的内容
    mblog=card['mblog']
    count_img=0# 每条微博重新计数图片数，用于发送图片的地址
    
    text= html.fromstring(mblog['text'])
    text=text.xpath('string(.)')#过滤正文中的多余标签
    
    url_img=''
    if 'pics' in mblog:#有图片的存储图片
        pics=mblog['pics']
        for pic in pics:
            url_img=pic['large']['url']
            ir = requests.get(url_img)
            if ir.status_code == 200:# 如果请求已成功
                count_img+=1# 给图片计数
                open('../img/'+str(count_img)+'.jpg', 'wb').write(ir.content)# 保存在img文件夹下，发送也从这个文件夹下找
            print u'图片：'+url_img
        
    scheme=card['scheme']
    created_at=mblog['created_at']
    source=mblog['source']
    reposts_count=mblog['reposts_count']
    comments_count=mblog['comments_count']
    attitudes_count=mblog['attitudes_count']
    
    return text,count_img,scheme,created_at,source,reposts_count,comments_count,attitudes_count# 其实返回的是一个list

def start_trans(start_i,start_j):# 两个参数分别为微博坐标，以便发布失败后断点续传
    #登录
    operator=weibo_op_driver.WBoperator()
    operator.login('15850782585', 'Weibo6981228.')
    crawl_wb=crawl_weibo.CrawlWeibo()
     
    for i in range(38)[start_i:]:
        page=38-i 
        cards=crawl_wb.getWeibo('2622535523',page)# 第一个参数是用户id，第二个是页数
        len_cards=len(cards)
         
        for j in range(len_cards)[start_j:]:
            index=len_cards-1-j
             
            card=cards[index]
             
            if card['card_type']==9 and not 'retweeted_status' in card['mblog']:# 如果是一条微博的card
                # 获取这条微博的内容
                content_list=getContent(card)
                text,count_img,scheme,created_at,source,reposts_count,comments_count,attitudes_count=content_list
                     
                #发送这条微博的内容到新账号
                text=u'#系统自动发布#原博文链接：'+scheme+'\n\n'+created_at+u'  来自 '+source+'\n\n'+text+' \n\n'+u'转发 '+str(reposts_count)+u'  评论 '+str(comments_count)+u'  点赞 '+str(attitudes_count)
                #打印
                print u'正在发布微博:('+str(i)+u','+str(j)+u')……'
                print text
                print '=============================='
                print '\n'
                 
                path_list=[]# 图片地址list
                for p in range(count_img):
                    path_list.append('C:\\Users\\15850\\Documents\\GitHub\\MyWorkspace\\py_study\\img\\'+str(p+1)+'.jpg')
                # 上传内容
                if count_img==0:
                    operator.upload_txt(text)
                elif count_img==1:
                    operator.upload_txt_img(text, path_list[0])
                else:
                    operator.upload_txt_multiImg(text,path_list)
                     
                operator.send()


# 上次断点 10,4
start_trans(35, 8)                