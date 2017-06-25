# -*- coding:utf-8 -*-
'''
Created on 2017年5月23日

@author: 15850
'''
# for x,y in enumerate([(1,2),(3,4),(5,4)]):
#     print(x,y)

# import urllib2
# from lxml import html
# import re
# 
# url='https://tieba.baidu.com/p/3267113128?see_lz=1&pn=2'
# user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
# headers={'User-Agent':user_agent}
# 
# request=urllib2.Request(url)
# response=urllib2.urlopen(request)
# str_html=response.read()
# response.close()
# 
# 
# re_num=re.compile('([0-9]\.)')
#  #666
# content_txt=content.xpath('string(.)')
 
import urllib2
from lxml import html
import re

class BaiduTieba:
    url_base='https://tieba.baidu.com/p/3267113128?see_lz='
    file = open("../text/bdtb.txt","w+")
    
    def __init__(self,see_lz):#see_lz=1表示只看楼主
        self.url_base=self.url_base+see_lz
    
    def setPage(self,page):
        self.url=self.url_base+'&pn='+page#目标url

    def printPage(self):
        request=urllib2.Request(self.url)#封装请求
        response=urllib2.urlopen(request)#打开url资源，得到响应
        str_html=response.read()#读取html文本内容
        response.close()#关闭资源
        
        str_html=unicode(str_html,'utf-8')#将string字符类型转换成unicode字符类型
        
        tree=html.fromstring(str_html)
        nodes=tree.xpath('//div[contains(@class,"d_post_content_main")]')#先找的所有的楼层再进一步解析楼层号码和内容
        
        re_num=re.compile('([0-9]\.)')
        for node in nodes:
            layer=node.xpath('div[@class="core_reply j_lzl_wrapper"]/div[@class="core_reply_tail clearfix"]/div[@class="post-tail-wrap"]/span[2]')[0].text
            
            self.file.write("\n")
            self.file.write("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\n")
            self.file.write("------------------------------------------------------------------------------------\n")
            self.file.write("                                  "+layer.encode("utf-8")+"                                         \n")
            self.file.write("------------------------------------------------------------------------------------\n")
            content=node.xpath('div[@class="p_content  "]/cc/div')[0]
            content_txt=content.xpath('string(.)')
            content_txt=re.sub(re_num,r'\n\1',content_txt)
        
            self.file.write(content_txt.encode("utf-8"))#输出楼层内容
            self.file.write("------------------------------------------------------------------------------------\n")


crawl_bdtb=BaiduTieba("1")
for i in range(5):#爬5页
    crawl_bdtb.setPage(str(i+1))
    crawl_bdtb.printPage()