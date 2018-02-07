# -*- coding:utf-8 -*-
'''
Created on 2017年5月24日

@author: 15850
'''
import requests
import json
from lxml import html
from bs4 import BeautifulSoup

class CrawlMusic163:
   
    #获取json解析出所有歌曲对象，返回歌曲的list
    def getSongs(self,id):#这里的id是歌单的id
        url = 'http://music.163.com/playlist?id='+str(id)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        ul = soup.select("ul.f-hide")[0]
        li_list = ul.find_all("li")

        songs_id = []
        for li in li_list:
            songs_id.append(li.select("a")[0]["href"])
        return songs_id

    #获取每首歌的热门评论的list
    def getHotComments(self, id):#这里的id是歌曲的id
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Host": "music.163.com",
            "Upgrade-Insecure - Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
        }

        url='http://music.163.com/weapi/v1/resource/comments/R_SO_4_'+str(id)+'?csrf_token=c0f6bfdcd0526ec0ba6c207051a08960'
        
        param={'params':'wxLqdGgw16OHb6UwY/sW16VtLqAhGaDMeI2F4DaESDplHA+CPsscI4mgiKoVCPuWW8lcd9eY0YWR/iai0sJqs0NmtLubVCkG\
        dpNTN3mLhevZpdZy/XM1+z7L18InFz5HbbRkq230i0aOco/3jVsMWcD3/tzzOCLkGuu5xdbo99aUjDxHwDSVfu4pz4spV2KonJ47Rt6vJhOorV7LfpIVmP/qeZghfaXXuKO2chlqU54=',\
        'encSecKey':'12d3a1e221cd845231abdc0c29040e9c74a47ee32eb332a1850b6e19ff1f30218eb9e2d6d9a72bd797f75fa115b769ad580fc51128cc9993e51276043ccbd9ca4e1f589a2ec479ab0323c973e7f7b1fe1a7cd0a02ababe2adecadd4ac93d09744be0deafd1eef0cfbc79903216b1b71a82f9698eea0f0dc594f1269b419393c0'}
        r =requests.post(url, headers=headers, data=param)
        data=r.text
        print(data)
        jsob=json.loads(data)#加载获取的json数据，获得json对象
        hotComments=jsob['hotComments']
  
        return hotComments
 
if __name__ == "__main__":
    crawl_music_163=CrawlMusic163()
    songs_id = crawl_music_163.getSongs(700734626)
    print(songs_id)
    # hotcomments = crawl_music_163.getHotComments("213347")
    # print(hotcomments)

    # for song in songs:
    #     hotComments=crawl_music_163.getHotComments(song['id'])#按id获取该歌曲的热门评论list
    #
    #     #输出每首歌的歌手名字-歌名-热门评论数
    #     print(song['artists'][0]['name']+"-"+song['name']+u"-热门评论："+str(len(hotComments)))
    #     print('########################################################################')
    #
    #     #每首歌循环输出所有热门评论
    #     for i in range(len(hotComments)):
    #         user_nickname=hotComments[i]['user']['nickname']
    #         likedCount=hotComments[i]['likedCount']
    #         content=hotComments[i]['content']
    #
    #         print(u'评论'+str(i+1)+u' 用户名:'+user_nickname+u" 喜欢:"+str(likedCount))
    #         print('------------------------------------------------------------------')
    #         print(content)
    #         print('------------------------------------------------------------------')
    #         print('\n')
    #     print('########################################################################')