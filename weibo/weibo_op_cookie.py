# -*- coding:utf-8 -*-
import pickle
import json
import requests
import re

class WeiboOpWithCoocie:
    def get_headers_edit(self, cookies):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Host": "account.weibo.com",
            "Referer": "https://account.weibo.com/set/iframe?skin=skin048",
            "Upgrade-Insecure - Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
        }

        cookie = ""
        for c in cookies:
            cookie = "%s;%s=%s" % (cookie, c["name"], c["value"])
        headers["Cookie"] = cookie[1:]  # 去掉首个分号
        print(json.dumps(cookies, indent=2))
        return headers

    def get_headers_post(self, cookies):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Host": "weibo.com",
            "Referer": "https://weibo.com",
            "Upgrade-Insecure - Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
        }

        cookie = ""
        for c in cookies:
            cookie = "%s;%s=%s" % (cookie, c["name"], c["value"])
        headers["Cookie"] = cookie[1:]  # 去掉首个分号
        return headers

    # 修改基本信息，没搞定，未知参数rid
    def edit_info(self, cookies):
        headers = self.get_headers_edit(cookies)
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
        res = requests.post("https://account.weibo.com/set/aj/iframe/editinfo", headers=headers, data=payload).text
        if res['code'] == '100000':
            print("edit_info success!")
            return True
        else:
            print("edit_info fail... " + res['msg'])
            return False

    # 修改教育信息
    def edit_edu(self, cookies):
        headers = self.get_headers_edit(cookies)
        payload = {'name': '北京外国语大学',
                   'school_type': '1',
                   'start': '1995',
                   'privacy': '2',
                   'school_province': '11',
                   'school_id': '243973',
                   }

        res = requests.post("https://account.weibo.com/set/aj/iframe/edupost", headers=headers, data=payload).text
        if res['code'] == '100000':
            print("edit_edu success!")
            return True
        else:
            print("edit_edu fail... " + res['msg'])
            return False

    # 发文字微博
    def post(self, text, cookies):
        headers = self.get_headers_post(cookies)

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
        res = requests.post("https://weibo.com/aj/mblog/add", headers=headers, data=payload).text
        res = json.loads(res)
        if res['code'] == '100000':
            print("post blog success!")
            return True
        else:
            print("post blog fail... " + res['msg'])
            return False
        
    # 给微博点赞
    def like_blog(self, blog_mid, cookies):
        headers = self.get_headers_post(cookies)
        payload = {
            'version': ' mini',
            'qid': ' heart', 
            'mid': blog_mid,
            'loc': ' profile', 
            'cuslike': ' 1', 
            '_t': ' 0', 
        }
        res = requests.post("https://weibo.com/aj/v6/like/add", headers=headers, data=payload).text
        res = json.loads(res)
        if res['code'] == '100000':
            print("like_blog success!")
            return True
        else:
            print("like_blog fail... " + res['msg'])
            return False

    #
    def like_object(self, ob_id, ob_type, cookies):
        headers = self.get_headers_post(cookies)
        payload = {
            'object_id': ob_id,
            'object_type': ob_type,
            '_t': '0',
        }
        res = requests.post("https://weibo.com/aj/v6/like/objectlike", headers=headers, data=payload).text
        res = json.loads(res)
        if res['code'] == '100000':
            print("like_object(%s) success!" % (ob_type))
            return True
        else:
            print("like_object(%s) fail... " % (ob_type) + res['msg'])
            return False

    # 给评论点赞（捞人，抢热门
    def like_comment(self, comment_id, cookies):
        self.like_object(comment_id, "comment", cookies)

    # 评论和转发
    def comment_forward(self, blog_mid, uid, content, forward, cookies):
        headers = self.get_headers_post(cookies)
        payload = {
            'act': 'post', 
            'mid': blog_mid,
            'uid': uid,
            'forward': forward,
            'isroot': '0', 
            'content': content,
            'module': 'scommlist',
            'group_source': '', 
            '_t': '0',
        }
        res = requests.post("https://weibo.com/aj/v6/comment/add", headers=headers, data=payload).text
        res = json.loads(res)
        if res['code'] == '100000':
            print("comment_forward success!")
            return True
        else:
            print("comment_forward fail... " + res['msg'])
            return False

    # 删除微博
    def del_blog(self, blog_mid, cookies):
        headers = self.get_headers_post(cookies)
        payload = {
            'mid': blog_mid,
        }
        res = requests.post("https://weibo.com/aj/mblog/del", headers=headers, data=payload).text
        res = json.loads(res)
        if res['code'] == '100000':
            print("del_blog success!")
            return True
        else:
            print("del_blog fail... " + res['msg'])
            return False

    # 删除微博的评论
    def del_comment(self, blog_mid, comment_id, uid, cookies):
        headers = self.get_headers_post(cookies)
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
        res = requests.post("https://weibo.com/aj/comment/del", headers=headers, data=payload).text
        res = json.loads(res)
        if res['code'] == '100000':
            print("del_comment success!")
            return True
        else:
            print("del_comment fail... " + res['msg'])
            return False

    # 关注和取关
    def follow_unfo(self, object_uid, follow, cookies):
        headers = self.get_headers_post(cookies)
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

        res = requests.post("https://weibo.com/aj/f/%s" % (follow), headers=headers, data=payload).text
        res = json.loads(res)
        if res['code'] == '100000':
            print("follow_unfo success!")
            return True
        else:
            print("follow_unfo fail... " + res['msg'])
            return False

    def home(self, uid, cookies):
        headers = self.get_headers_post(cookies)
        print(requests.get("https://weibo.com/u/%s/home" % (uid), headers=headers).text)

    def get_uid(self, cookies):
        uid = ""
        for c in cookies:
            match_ob = re.match("wb_cusLike_([0-9]*)", c['name'])
            if match_ob is not None:
                uid = match_ob.group(1)
        if uid != "":
            print(uid)
        else:
            print(u"出错了，没有从cookies中获取到uid...")
        return uid

if __name__ == "__main__":
    cookies = pickle.load(open("./co_182", "rb"))
    wbop = WeiboOpWithCoocie()
    # wbop.del_comment("4196497862202988", "4196499850359603", wbop.get_uid(cookies), cookies)
    wbop.follow_unfo("6219737121", "1", cookies)
    # wbop.comment_forward("4196060278136857", wbop.get_uid(cookies), u"好暖呢", "1", cookies)
    # headers = wbop.like_comment("4196488429169417", co)