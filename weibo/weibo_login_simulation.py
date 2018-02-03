# -*- coding:utf-8 -*-
import rsa
import binascii
import time
from urllib import parse
import requests
import re
import json
import logging
import base64
from weibo.weibo_database import DBManager
from weibo.weibo_op import WeiboOp
import random

class WeiboLoginSimulation:
    def __init__(self):
        self.session = requests.session()
        self.user_uniqueid = ""
        self.user_nick = ""
        pass

    def prelogin(self, username_encoded):
        url = "http://login.sina.com.cn/sso/prelogin.php"
        payload = {
            "entry": "weibo",
            "callback": "sinaSSOController.preloginCallBack",
            "su": username_encoded,
            "rsakt": "mod",
            "checkpin": "1",
            "client": "ssologin.js(v1.4.19)",
            "_": int(time.time()*1000),
        }
        res = self.session.post(url, data=payload, )
        prelogin_json = re.search("\((.*)\)", res.text).group(1)

        return json.loads(prelogin_json)

    def get_username(self, username):
        return base64.b64encode(parse.quote_plus(username).encode("utf-8"))

    def get_password(self, pass_word, servertime, nonce, pubkey):
        string = (str(servertime) + "\t" + str(nonce) + "\n" + str(pass_word)).encode("utf-8")
        public_key = rsa.PublicKey(int(pubkey, 16), int("10001", 16))
        password = rsa.encrypt(string, public_key)
        password = binascii.b2a_hex(password)
        return password.decode()

    def identify_captcha(self, cap_b64):
        typeid = 35
        appkey = "f1d9b361016be2d78f0684fb5891f2c3"
        url = "https://way.jd.com/showapi/checkcode_ys?typeId=%d&convert_to_jpg=0&appkey=%s" % (typeid, appkey)

        payload = {
            "body": "img_base64=%s" % cap_b64,
        }
        res = requests.post(url, data=payload)
        res_js = res.json()
        if res_js["code"] == "10000" and res_js["result"]["showapi_res_code"] == 0 and res_js["result"]["showapi_res_body"]["ret_code"] == 0:
            return res_js["result"]["showapi_res_body"]["Result"]
        else:
            logging.warning(res_js)
            return None

    def login_request(self, username_encoded, pw_encrypted, prelogin_json):
        url_login = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)&wsseretry=servertime_error"
        payload = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "userticket": "1",
            "vsnf": "1",
            "service": "miniblog",
            "encoding": "UTF-8",
            "pwencode": "rsa2",
            "sr": "1280*800",
            "prelt": "529",
            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "rsakv": prelogin_json["rsakv"],
            "servertime": prelogin_json["servertime"],
            "nonce": prelogin_json["nonce"],
            "su": username_encoded,
            "sp": pw_encrypted,
            "returntype": "TEXT",
        }

        # 判断验证码
        json_ticket = None
        if "showpin" in prelogin_json and prelogin_json["showpin"] == 1: # 如果需要输入验证码
            payload["pcid"] = prelogin_json["pcid"]

            url_pin = "http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s" % (
            int(time.time() * 1000), prelogin_json["pcid"])  # 获得验证码的地址

            res = self.session.post(url_pin, data=payload)
            captcha_img = open("./captcha.png", "wb")
            captcha_img.write(res.content)
            captcha_img.close()

            captcha_img_b64 = base64.b64encode(res.content).decode()
            iden = self.identify_captcha(captcha_img_b64)

            code = ""
            if iden is None:
                code = input("请输入验证码:")
            else:
                code = iden

            payload["door"] = code

        # login weibo.com
        res = self.session.post(url_login, data=payload)
        json_ticket = res.json()
        if json_ticket["retcode"] != "0":
            logging.warning("WeiBoLogin failed: %s", json_ticket)
            return False
        else:
            params = {
                "callback": "sinaSSOController.callbackLoginStatus",
                "client": "ssologin.js(v1.4.19)",
                "ticket": json_ticket["ticket"],
                "ssosavestate": int(time.time()),
                "_": int(time.time() * 1000),
            }
            response = self.session.get("http://passport.weibo.com/wbsso/login", params=params)
            json_data_2 = json.loads(re.search(r"\((?P<result>.*)\)", response.text).group("result"))
            if json_data_2["result"] is True:
                self.user_uniqueid = json_data_2["userinfo"]["uniqueid"]
                self.user_nick = json_data_2["userinfo"]["displayname"]
                logging.warning("WeiBoLogin succeed: %s", json_data_2)
                return True
            else:
                logging.warning("WeiBoLogin failed: %s", json_data_2)
                return False
    def home(self):
        res = self.session.get("https://weibo.com/u/%s/home" % (self.user_uniqueid)).text
        if u"我的首页" in res:
            return True
        else:
            return False

    def login_simulate(self, username, pw):
        while True:
            username_encoded = self.get_username(username)
            prelogin_json = self.prelogin(username_encoded)
            pw_encrypted = self.get_password(pw, prelogin_json["servertime"], prelogin_json["nonce"],
                                             prelogin_json["pubkey"])

            login_res = self.login_request(username_encoded, pw_encrypted, prelogin_json)
            if login_res and self.home(): # 一旦登录成功就返回user
                return {"uid": self.user_uniqueid, "session": self.session} # 返回登录的user的dict
            else:
                logging.warning("login failed, try again...")

    # 将登录成功后的cookies_dict保存到数据库
    def save_cookies(self, accounts_file_path, level):
        f = open(accounts_file_path, "r")
        db = DBManager()

        for line in f:
            line = line.strip()
            match_ob = re.match("([0-9]+)----(.*)", line)
            username = match_ob.group(1)
            password = match_ob.group(2)

            if db.count(username) == 0:
                user = self.login_simulate(username, password)
                if user is not None:
                    cookies_dict = user["session"].cookies.get_dict()
                    cookies_json = json.dumps(cookies_dict)
                    wbop = WeiboOp(user["uid"], session=user["session"])
                    wbop.check_level() # 看一看等级，升级到4级

                    db.insert_account(cookies_json, username, password, level, user["uid"])

                    self.random_wait(30)
                else:
                    logging.warning("login failed...")


        db.db_close()

    def random_wait(self, base):
        random.seed(time.time())
        sleeptime = base + 30 * random.random()
        print("sleep %ds" % sleeptime)
        time.sleep(sleeptime)

    # 检查数据库里的cookies 的有效性
    def check_cookies(self, level):
        db = DBManager()
        accounts = db.get_accounts(level)

        for account in accounts:
            cookies_dict = json.loads(account[0])
            uid = account[1]
            wbop = WeiboOp(uid, cookies=cookies_dict)
            login_res = wbop.home()
            print(login_res)

            self.random_wait(30)
if __name__ == "__main__":
    wbls = WeiboLoginSimulation()
    # wbls.save_cookies("./accounts.txt", 3)
    # login_res = wbls.login_simulate("18773079305", "WWWEEE6981228.")

