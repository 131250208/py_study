# -*- coding:utf-8 -*-

import requests
import json
from lxml import html
import time


def search(src_name,page):
    url_api = "https://m.wangpan007.com/search/ajax?keyword="+src_name+"&page="+str(page)
    responce = requests.get(url_api)
    if responce.status_code == 200 :
        return json.loads(responce.text)
    else:
        print "failure...request again"
        return search(src_name,page)

# 爬取所有资源，返回五元组list
def search_all(src_name):
    jsob = search(src_name,1)
    pageCount = jsob["pageCount"]
    src_cnt = 0
    if pageCount == 0 :
        return None
    else:
        cache = []  # 用来暂时存放资源数据，以待进一步处理

        for p in range(1,pageCount+1):
            jsob = search(src_name,p)
            src_list = jsob["list"]
            for src in src_list:
                src_cnt += 1
                filename = src["filename"]
                filename = html.fromstring(filename).xpath("string(.)")
                share_cat = src["share_cat"]
                share_url = src["share_url"]
                size = src["size"]
                view_cnt = src["vcnt"]
                download_cnt = src["dcnt"]
                transfer_cnt = src["tcnt"]
                created = src["created"]
                created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created/1000))
                feed_time = src["feed_time"]
                feed_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(feed_time/1000))
                suffix = src["suffix"][1:]

                info =str(feed_time) + u"  " + str(view_cnt) + u"次浏览/" + str(download_cnt) + u"次下载/" + str(transfer_cnt) + u"次转存"
                URL = share_url
                heat = 0.3*view_cnt + 0.4*download_cnt + 0.3*transfer_cnt
                cache.append({'name': filename, 'url': URL, 'cat': suffix, 'info': info, 'heat': heat})# 加进缓存list

                # if not os.path.exists(u"../text/" + src_name + u"_资源链接文档合集" + u"/" + share_cat):
                #     os.makedirs(u"../text/" + src_name + u"_资源链接文档合集" + u"/" + share_cat)
                #
                # file =codecs.open(u"../text/" + src_name + u"_资源链接文档合集" + u"/" + share_cat + u"/" + suffix + u".txt", 'a+',"utf-8")
                # file.write(u"资源编号: " + str(src_cnt) + "\n")
                # file.write(u"资源名称: \n" + filename + u"\n\n")
                # file.write(u"链接地址: \n" + share_url + u"\n")
                # file.write("---------------------------------\n\n")
                #
                print str(src_cnt) + "-----------------------------"
                print u"资源名称" + filename
                print u"链接" + share_url
                print u"资源种类" + share_cat
                print u"文件大小" + str(size)
                print u"浏览次数" + str(view_cnt)
                print u"下载次数" + str(download_cnt)
                print u"转存次数" + str(transfer_cnt)
                print u"" + str(created)
                print str(feed_time)
                print "---------------------------------\n"

        # make_zip(u"../text/" + src_name + u"_资源链接文档合集",u"../text/" + src_name + u"_资源链接文档合集.zip")

        return cache

search_all(u"欢乐颂")