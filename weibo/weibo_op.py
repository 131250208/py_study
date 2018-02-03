# -*- coding:utf-8 -*-
import pickle
import json
import requests
import re
from weibo.weibo_database import DBManager
import time
import base64
import random

class WeiboOp:

    def __init__(self, uid, session=None, cookies=None):# 传入已登录的session 或者 登录状态的cookies的dict
        self.uid = uid
        if session is None:
            self.session = requests.session()
            if cookies is not None:
                requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies)
        else:
            self.session = session

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Host": "weibo.com",
            "Referer": "https://weibo.com/",
            "Upgrade-Insecure - Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
        }

        self.session.headers.update(headers)


    # 修改基本信息，没搞定，未知参数rid
    def edit_info(self):
        payload = {
            'setting_rid': 'd1Vlf235Q-LBj/DshHM8stx-1GQ=',
            'nickname': '睡小迪_爱琪琪阿四',
            'realname': '薛梦雪',
            'gender': 'f',
            'sextrend[]': '0',
            'blog': '',
            'mydesc': '一心一意',
            'province': '11',
            'city': '1',
            'love': '',
            'Date_Year': '1998',
            'birthday_m': '03',
            'birthday_d': '06',
            'blood': '',
            'pub_name': '0',
            'pub_sextrend': '0',
            'pub_love': '1',
            'pub_birthday': '3',
            'pub_blood': '1',
            'pub_blog': '2',
        }
        res = self.session.post("https://account.weibo.com/set/aj/iframe/editinfo", headers={"Host": "account.weibo.com",}, data=payload).text
        if res['code'] == '100000':
            print("edit_info success!")
            return True
        else:
            print("edit_info fail... " + res['msg'])
            return False

    # 修改教育信息
    def edit_edu(self):
        payload = {'name': '北京外国语大学',
                   'school_type': '1',
                   'start': '2014',
                   'privacy': '2',
                   'school_province': '11',
                   'school_id': '243973',
                   }

        res = self.session.post("https://account.weibo.com/set/aj/iframe/edupost", headers={"Host": "account.weibo.com",}, data=payload).text
        try:
            res = json.loads(res)
            if res['code'] == '100000':
                print("edit_edu success!")
                return True
            else:
                print("edit_edu fail... " + res['msg'])
                return False
        except:
            print(res)
            return False

    # 发文字微博
    def post(self, text):

        payload = {
            'text': text,
            'appkey': '', 
            'style_type': '1', 
            'pic_id': '', 
            'tid': '', 
            'pdetail': '', 
            'rank': '0', 
            'rankid': '', 
            'module': 'stissue', 
            'pub_source': 'main_', 
            'pub_type': 'dialog', 
            'isPri': '0', 
            '_t': '0', 
        }
        res = self.session.post("https://weibo.com/aj/mblog/add", data=payload).text
        res = json.loads(res)
        if res['code'] == '100000':
            print("post blog success!")
            return True
        else:
            print("post blog fail... " + res['msg'])
            return False
        
    # 给微博点赞
    def like_blog(self, blog_mid):
        payload = {
            'version': ' mini',
            'qid': ' heart', 
            'mid': blog_mid,
            'loc': ' profile', 
            'cuslike': ' 1', 
            '_t': ' 0', 
        }
        res = self.session.post("https://weibo.com/aj/v6/like/add", data=payload).text
        res = json.loads(res)
        if res['code'] == '100000':
            print("%s like_blog %s success!" % (self.uid, blog_mid))
            return True
        else:
            print("%s like_blog %s fail... msg: %s" % (self.uid, blog_mid, res['msg']))
            return False

    #
    def like_object(self, ob_id, ob_type):
        payload = {
            'object_id': ob_id,
            'object_type': ob_type,
            '_t': '0',
        }
        res = self.session.post("https://weibo.com/aj/v6/like/objectlike", data=payload).text
        res = json.loads(res)
        if res['code'] == '100000':
            print("like_object(%s) success!" % (ob_type))
            return True
        else:
            print("like_object(%s) fail... " % (ob_type) + res['msg'])
            return False

    # 给评论点赞（捞人，抢热门
    def like_comment(self, comment_id):
        self.like_object(comment_id, "comment")

    # 评论和转发
    def comment_forward(self, blog_mid, content, forward, img_url=None, img_id=None): # 目标微博id, 评论者的uid，评论内容，forward = {"0", "1"}是否转发
        payload = {
            'act': 'post', 
            'mid': blog_mid,
            'uid': self.uid,
            'forward': forward,
            'isroot': '0', 
            'content': content,
            'module': 'scommlist',
            'group_source': '', 
            '_t': '0',
        }
        if img_url is not None:
            pic_id = self.up_img(img_url)
            payload["pic_id"] = pic_id
        if img_id is not None:
            payload["pic_id"] = img_id

        res = self.session.post("https://weibo.com/aj/v6/comment/add", data=payload)
        print(res.text)
        res = json.loads(res.text)
        if res['code'] == '100000':
            print("comment_forward success! comments: %s" % content)
        else:
            print("comment_forward fail... " + res['msg'])
        return res

    #
    def img_bs64(self, url):
        ls_f = ""
        if "http" in url:# 网络地址
            content = requests.get(url).content
            ls_f = base64.b64encode(content)  # 读取文件内容，转换为base64编码

        else:# 本地地址
            f = open(url, 'rb')  # 二进制方式打开图文件
            ls_f = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
            f.close()
        img_bs64_str = ls_f.decode()  # 解码成字符串

        return img_bs64_str

    # 上传图片获取pic_id
    def up_img(self, img_url):
        img_bs64_str = self.img_bs64(img_url)

        url = "https://picupload.weibo.com/interface/pic_upload.php"
        payload = {
            "cb": "https://weibo.com /aj/static/upimgback.html?_wv=5&callback=STK_ijax_151694642763479",
            "mime": "image/jpeg",
            "data": "base64",
            "url": "weibo.com/u/%s" % self.uid,
            "markpos": "1",
            "logo": "1",
            # "nick": "@王雨城_Vision_Wong",
            "marks": "1",
            "app": "miniblog",
            "s": "rdxt",
            "file_source": "3",
        }

        img = {
            "b64_data": img_bs64_str,
        }
        try:
            res = self.session.post(url, data=payload, files=img)
        except Exception as e:
            return re.search("&pid=([\S]*)", str(e)).group(1)# 从异常信息中可以得到返回的pid

    # 删除微博
    def del_blog(self, blog_mid):
        payload = {
            'mid': blog_mid,
        }
        res = self.session.post("https://weibo.com/aj/mblog/del", data=payload).text
        res = json.loads(res)
        if res['code'] == '100000':
            print("del_blog success!")
            return True
        else:
            print("del_blog fail... " + res['msg'])
            return False

    # 删除微博的评论
    def del_comment(self, blog_mid, comment_id, uid):
        payload = {
            'act': 'delete', 
            'mid': blog_mid,
            'cid': comment_id,
            'uid': uid,
            'is_block': '0', 
            'rid': comment_id,
            'oid': '', 
            '_t': '0', 
        }
        res = self.session.post("https://weibo.com/aj/comment/del", data=payload).text
        res = json.loads(res)
        if res['code'] == '100000':
            print("del_comment success!")
            return True
        else:
            print("del_comment fail... " + res['msg'])
            return False

    # 关注和取关
    def follow_unfo(self, object_uid, follow):
        payload = {
            'uid': object_uid,
            'refer_flag': '1005050002',
            'oid': object_uid,
            'wforce': '1', 
            'nogroup': 'false', 
            'refer_from': 'profile_headerv6',
            '_t': '0', 
        }
        if follow == "1":
            follow = "followed"
        elif follow == "0":
            follow = "unfollow"
        res = self.session.post("https://weibo.com/aj/f/%s" % (follow), data=payload).text
        res = json.loads(res)
        if res['code'] == '100000':
            print("follow_unfo success!")
            return True
        else:
            print("follow_unfo fail... " + res['msg'])
            return False

    def home(self):
        res = self.session.get("https://weibo.com/u/%s/home" % (self.uid)).text
        # print(res)
        if u"我的首页" in res:
            return True
        else:
            return False

    # 进入微博等级页面再回到主页，等级可升到4级
    def check_level(self):
        for i in range(3):
            self.session.get("http://level.account.weibo.com/level/mylevel?from=front", headers={"Host": "level.account.weibo.com"})
        self.home()

if __name__ == "__main__":
    pass
    # cookies = pickle.load(open("./co_158", "rb"))
    # wbop = WeiboOpWithCoocie()
    # wbop.home(wbop.get_uid(cookies), cookies)
    # wbop.del_comment("4196497862202988", "4196499850359603", wbop.get_uid(cookies), cookies)
    # wbop.follow_unfo("6219737121", "1", cookies)
    # wbop.comment_forward("4196060278136857", wbop.get_uid(cookies), u"好暖呢", "1", cookies)
    # headers = wbop.like_comment("4196488429169417", co)

    # db = DBManager()
    # wbop = WeiboOpWithCoocie()
    # cookies_uid_list = db.get_accounts(3)

    # for ind, cookies_uid in enumerate(cookies_uid_list):
    #     time.sleep(3.5)
    #     cookies = json.loads(cookies_uid[0])
    #     # wbop.comment_forward("4196631999963758", cookies_uid[1], contents[ind], "0", cookies)
    #     # wbop.like_blog("4196631999963758", cookies)
    #     print(wbop.home(cookies_uid[1], cookies))

    # cookies_uid_list = db.get_cookies_uid("13786733392")
    # cookies = json.loads(cookies_uid_list[0][0])
    # home_page = wbop.home(cookies_uid_list[0][1], cookies)
    # print(home_page)