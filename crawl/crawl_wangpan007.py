# -*- coding:utf-8 -*-

import requests
import json
from lxml import html
import time
import os
import codecs
import zipfile

def search(src_name,page):
    url_api = "https://m.wangpan007.com/search/ajax?keyword="+src_name+"&page="+str(page)
    responce = requests.get(url_api)
    if responce.status_code == 200 :
        return json.loads(responce.text)
    else:
        print "failure...request again"
        return search(src_name,page)

def search_all(src_name):
    jsob = search(src_name,1)
    pageCount = jsob["pageCount"]
    src_cnt = 0
    if pageCount == 0 :
        return None
    else:
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

                if not os.path.exists(u"../text/" + src_name + u"_资源链接文档合集" + u"/" + share_cat):
                    os.makedirs(u"../text/" + src_name + u"_资源链接文档合集" + u"/" + share_cat)

                file =codecs.open(u"../text/" + src_name + u"_资源链接文档合集" + u"/" + share_cat + u"/" + u"资源种类:" + suffix + u".txt", 'a+',"utf-8")
                file.write(u"资源编号: " + str(src_cnt) + "\n")
                file.write(u"资源名称: \n" + filename + u"\n\n")
                file.write(u"相关信息: \n" + str(feed_time) + u"  " + str(view_cnt) + u"次浏览/" + str(download_cnt) + u"次下载/" + str(transfer_cnt) + u"次转存\n\n")
                file.write(u"链接地址: \n" + share_url + u"\n")
                file.write("---------------------------------\n\n")
                
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

        make_zip(u"../text/" + src_name + u"_资源链接文档合集",u"../text/" + src_name + u"_资源链接文档合集.zip")

# 打包目录为zip文件（未压缩）
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()
                


# try:
search_all(u"欢乐颂")
# except:
#     print "something wrong!"