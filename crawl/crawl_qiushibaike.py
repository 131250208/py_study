    # -*- coding:utf-8 -*-

import urllib
import urllib2
from lxml import html

# timeout = 20 
# socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置  
# sleep_download_time = 10
# time.sleep(sleep_download_time) #这里时间自己设定  

     
page=1
url='http://www.qiushibaike.com/hot/page/'+str(page)
user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
headers={'User-Agent':user_agent}

request=urllib2.Request(url,headers=headers)
response=urllib2.urlopen(request)
str_html= response.read()
response.close()

tree=html.fromstring(str_html)
nodes=tree.xpath('//div[@id="content-left"]/div[@class="article block untagged mb15"]')
for node in nodes:
    res_author=node.xpath('div[@class="author clearfix"]/a[2]/h2')[0].text
    content=node.xpath('a[@class="contentHerf"]/div[@class="content"]/span')[0].text
    num_vote=node.xpath('div[@class="stats"]/span[@class="stats-vote"]/i')[0].text
    num_comments=node.xpath('div[@class="stats"]/span[@class="stats-comments"]/a[@class="qiushi_comments"]/i')[0].text  
    print u"作者："+res_author
    print "---------------------------------------------------------"
    print u"内容："+content  
    print "---------------------------------------------------------"
    print u"点赞："+num_vote+u",评论："+num_comments+"\n"
