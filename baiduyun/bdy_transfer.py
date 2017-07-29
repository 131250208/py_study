# -*- coding:utf-8 -*-
import requests
import json
import bs4
from selenium import webdriver

class BaiduYunTransfer:

    headers = None


    def __init__(self,bduss,stoken):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '161',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'BDUSS=%s;STOKEN=%s;' % (bduss, stoken),
            'Host': 'pan.baidu.com',
            'Origin': 'https://pan.baidu.com',
            'Referer': 'https://pan.baidu.com/s/1dFKSuRn?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
    def getFilelist(self,url_src):
        driver = webdriver.PhantomJS()
        driver.viewportSize = {'width': 1024, 'height': 800}  # 重要这句！
        driver.maximize_window()
        driver.implicitly_wait(10)  # 设置隐性等待时间，等待页面加载完成才会进行下一步，最多等待10秒

        driver.get(url_src)# 貌似是反爬虫的机制，第一次get的是“页面不存在了”，request请求也是同样的结果
        driver.get(url_src)# 多刷新一次才会加载出来

        a_list = driver.find_elements_by_class_name("filename")

        filelist_mid = u""
        for a in a_list:
            rsc_path = u'"/我的资源/%s",' % (a.get_attribute("title"))
            filelist_mid += rsc_path

        filelist = u"[" + filelist_mid[:-1] + u"]"

        print filelist
        return filelist

    def transfer(self,bdstoken,share_id,uk,filelist_str,path_t_save):
        # 通用参数
        ondup = "newcopy"
        async = "1"
        channel = "chunlei"
        clienttype = "0"
        web = "1"
        app_id = "250528"
        logid = "MTUwMTMyODM3MTAxMDAuNzUyMzEwNjczOTQyOTUyNg=="
        url_trans = "https://pan.baidu.com/share/transfer?shareid=%s" \
                    "&from=%s" \
                    "&ondup=%s" \
                    "&async=%s" \
                    "&bdstoken=%s" \
                    "&channel=%s" \
                    "&clienttype=%s" \
                    "&web=%s" \
                    "&app_id=%s" \
                    "&logid=%s" % (share_id, uk, ondup, async, bdstoken, channel, clienttype, web, app_id, logid)

        form_data = {
            'filelist': filelist_str,
            'path': path_t_save,
        }
        response = requests.post(url_trans, data=form_data, headers=self.headers)
        print response.content
        jsob = json.loads(response.content)

        if jsob["errno"] == 0 :
            return True
        else:
            return False



bduss = '1hqMHBLQXF-bE9rSGFHeTBPcVppZm5YMVJaLXVwRjU4SS1rT0Z2ZWtnM3NDS1JaSUFBQUFBJCQAAAAAAAAAAAEAAACzoEC5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOx7fFnse3xZc'  ####详细见文章底部的图。打开chrome，登录帐号，按F12打开开发者工具，切换到network找一个动态请求地址，在RequestHeaders里找Cookie
stoken = '8926f7b79604743d22903d79a592087af3b455eef8cc8b123aa72a1abe0b5045'
bdy_trans = BaiduYunTransfer(bduss,stoken)
bdstoken = "f3d271200773bef0da3ef43aa252e33f"
share_id = "3344623723" # script里面
uk = "140959320" # script里面

url_src = "http://pan.baidu.com/s/1slVtmep"
filelist = bdy_trans.getFilelist(url_src)
path = u"/电影"

if bdy_trans.transfer(bdstoken,share_id,uk,filelist,path):
    print u"转存成功！"
else:
    print u"转存失败了，未知原因……"





