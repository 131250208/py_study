# -*- coding:utf-8 -*-
'''
Created on 2017年6月25日

用webdriver实现的各种微博操作
此类必须先执行login方法，其他方法才能正常使用
@author: wycheng
'''
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import re
import time
import pickle
import requests
import json
from weibo.weibo_database import DBManager
from weibo.weibo_op import WeiboOpWithCoocie

class WBoperator:
#     driver = webdriver.PhantomJS(service_args=['--remote-debugger-port=9001'])# chrome浏览器驱动
    def __init__(self):
        self.driver = webdriver.Chrome()# chrome浏览器驱动
        self.driver.implicitly_wait(10)# 设置隐性等待时间，等待页面加载完成才会进行下一步，最多等待10秒
        self.driver.set_window_size(1920, 1080)# 用phantomjs必须有这行
        self.wait=WebDriverWait(self.driver,10)
        self.uid_login=''# 登录后会赋予登录用户的id值
        pass
    
    # 根据验证框的存在与否判断是否要输入验证码
    def isVerifyCodeExist(self):
        try:# 如果成功找到验证码输入框返回true
            self.driver.find_element_by_css_selector('input[name="verifycode"]')
            return True
        except:# 如果异常返回false
            return False
    
    # 输入验证码部分，如果无需输入则直接返回，否则手动输入成功后返回        
    def inputVerifyCode(self):
        input_verifycode=self.driver.find_element_by_css_selector('input[name="verifycode"]')# 验证码输入框
        bt_change=self.driver.find_element_by_css_selector('img[action-type="btn_change_verifycode"]')# 验证码图片，点击切换
        bt_logoin=self.driver.find_element_by_class_name('login_btn')# 登录按钮
        while self.isVerifyCodeExist():
            print(u'请输入验证码……')
            # 截屏以便手动输入验证码
            verifycode = input()
            if verifycode=='OVER':
                break

        return self.driver.get_cookies()
    
    # 打开微博首页进行登录的过程
    def login(self,account,password):

        self.driver.delete_all_cookies()
        time.sleep(1)
        url='http://weibo.com/login.php'
        self.driver.get(url)
        
        # 输入账号密码并登录
        loginname=self.wait.until(lambda x:x.find_element_by_id('loginname'))
        loginname.send_keys(account)
        self.driver.find_element_by_css_selector('input[type="password"]').send_keys(password)
         
        bt_logoin=self.driver.find_element_by_class_name('login_btn')
        bt_logoin.click()
         
        # 如果存在验证码，则进入手动输入验证码过程
        if self.isVerifyCodeExist():
            return self.inputVerifyCode()

        time.sleep(2)

        return self.driver.get_cookies()
        # api调用次数受限，暂时不通过api
#         # 登录成功以后读取用户昵称，调用api获取用户id
#         username=self.driver.find_element_by_xpath('//a[@class="gn_name"]/em[2]').get_attribute('innerHTML')
#         self.uid_login=weibo_api.getID(username)
        
        # 用正则匹配找到登录用户的uid
        # time.sleep(0.5)# 稍等加载
        # scripts=self.driver.find_elements_by_xpath('//head/script')
        # str_script=scripts[-1].get_attribute('innerHTML')
        #
        # compile=re.compile('\[\'uid\'\]=\'[0-9]*\'')# 正则匹配的表达式
        # print(str_script)
        # uid_str=re.search(compile, str_script).group()# 匹配结果['uid']='6219737121'
        # uid=uid_str.split('=')[1][1:-1]
        #
        # self.uid_login=uid
    # 上传文字
    def upload_txt(self,text):
        input_w=self.driver.find_element_by_xpath('//div[@node-type="textElDiv"]/textarea[@class="W_input"]')
        input_w.send_keys(text)
        time.sleep(1)
    
    #运行上传图片脚步
    def upload_img_script(self,time_bef,time_after,path):# path参数需要前后带双引号
        time.sleep(time_bef)# 等待弹窗时间
        os.system('C:/Users/15850/Documents/GitHub/MyWorkspace/py_study/script/upload.exe '+path)
        time.sleep(time_after)# 等待图片加载时间
        
    # 上传文字和单图
    def upload_txt_img(self,text,img_path):
        self.upload_txt(text)# 将文字上传
        img=self.driver.find_element_by_css_selector('a[action-type="multiimage"]')# 图片按钮
        img.click()# 点击图片按钮
        time.sleep(1)# 等待加载其他按钮
        
        #单图/多图按钮，即上传图片按钮
        bt_uploadimg=WebDriverWait(self.driver,10).until(lambda x:x.find_element_by_xpath('//object[contains(@id,"swf_upbtn")]'))
        bt_uploadimg.click()# 点击上传按钮
        
        self.upload_img_script(1,5,img_path)
    
    # 上传文字和多图    
    def upload_txt_multiImg(self,text,img_path_list):
        self.upload_txt_img(text,img_path_list[0])# 将文字和第一张图片上传
       
        len_imgs=len(img_path_list)# 图片地址list的长度    
        bt_uploadimg=WebDriverWait(self.driver,10).until(lambda x:x.find_element_by_xpath('//li[@node-type="uploadBtn"]/div/object[contains(@id,"swf_upbtn")]'))
        for i in range(len_imgs-1):# 将剩余图片上传 
            bt_uploadimg.click()
            
            time_af=2
            if i==len_imgs-2:
                time_af=5
            self.upload_img_script(1, time_af,img_path_list[i+1])
    
    # 发布
    def send(self):
        self.driver.find_element_by_class_name('W_btn_a').click()
        time.sleep(4)# 等待发送成功字样消失

    
    # 批量删除微博
    def delete(self,num):
        # 进入到微博列表页面
        self.driver.find_element_by_xpath('//strong[@node-type="weibo"]').click()
        time.sleep(5)
        for i in range(num):
            # 找到最新一条微博的下拉选项按钮
#             last_weibo=self.driver.find_element_by_xpath('//div[contains(@id,"Pl_Official_MyProfileFeed")]/div[@node-type="feed_list"]/div[2]')
            try:
                self.driver.find_element_by_xpath('//a[@action-type="fl_menu"][1]').click()
                time.sleep(0.2)
                self.driver.find_element_by_xpath('//a[@action-type="feed_list_delete"]').click()
                time.sleep(0.2)
                self.driver.find_element_by_xpath('//a[@action-type="ok"]').click()
                time.sleep(1)
            except:
                continue
    
    
    # 关注用户
    def follow(self,uid):
        self.driver.get('http://weibo.com/u/'+uid)
        try:
            focuslink=self.wait.until(lambda x:x.find_element_by_xpath('//div[@node-type="focusLink"]/a'))
            focuslink.click()
            # 点完关注后，检查页面是否有需要输入验证码，如果有的话，等待2分钟重新关注该用户
            try:
                title=self.wait.until(lambda x:x.find_element_by_class_name('W_layer_title'))
                title_txt=title.get_attribute('innerHTML')
                if title_txt==u'关注成功':
                    print(u'关注用户：'+uid+u' 成功！')
                elif title_txt==u'请输入验证码':
                    print(u'需要输入验证码，等待120s……')
                    time.sleep(120)# 休息两分钟再试一次
                    print(u'等待结束，重试')
                    self.follow(uid)
            except:
                pass
        except:
            pass

    # 批量关注（参数可能包含已关注用户和自身id）
    def follow_uidlist(self,uid_list):# 参数为uid的一个list
        for uid in uid_list:
            if uid==self.uid_login:# 如果是自己的id，跳过
                continue
            
            # api接口受限，暂不使用
    #             str_frship=weibo_api.getFriendship(self.uid_login, uid)
    #             if str_frship!='api error':
    #                 if str_frship=='1:0' or str_frship=='1:1' :# 如果是已关注或者互相关注的用户，则跳过
    #                     continue
    #             else:
    #                 print('api error')
        
            # 是未关注用户，则关注
            self.follow(uid)

    # 取消关注
    def unfollow(self,uid):
        self.driver.get('http://weibo.com/u/'+uid)
        try:
            focuslink=self.wait.until(lambda x:x.find_element_by_xpath('//div[@node-type="focusLink"]/a'))
            focuslink.click()
            time.sleep(0.5)
            cancel_attan=self.wait.until(lambda x:x.find_element_by_xpath('//a[@suda-data="key=tblog_profile_v6&value=cancel_atten"]'))
            cancel_attan.click()
        except:
            pass
    
    # 批量取关
    def unfollow_uidlist(self,uid_list):
        for uid in uid_list:
            if uid==self.uid_login:# 如果是自己的id，跳过
                continue
            
            # api受限，暂不使用
#             str_frship=weibo_api.getFriendship(self.uid_login, uid)
#             if str_frship!='api error':
#                 if str_frship=='0:0' or str_frship=='0:1' :# 如果是没有关注过的，则跳过
#                     continue
#             else:
#                 print('api error')
            # 是已关注的用户，则取消关注
            self.unfollow(uid)
            
    # 获取某用户的关注列表（uid_list
    def get_followlist(self,uid,page):# uid：用户的id page；用户关注列表的翻页参数
        url='http://weibo.com/p/100505'+uid+'/follow'+'?page='+str(page)# 关注列表页
        self.driver.get(url)
        li_list=self.driver.find_elements_by_xpath('//ul[@node-type="userListBox"]/li')
        
        uid_list=[]
        for li in li_list:
            action_data=li.get_attribute('action-data')
            uid=action_data.split('&')[0].split('=')[1]
            uid_list.append(uid)
            
        return uid_list

    # 获取某用户的关注列表中 登录用户未关注的用户
    def get_followlist_unf(self,uid,page):
        url='http://weibo.com/p/100505'+uid+'/follow'+'?page='+str(page)# 关注列表页
        self.driver.get(url)
        a_list=self.driver.find_elements_by_xpath('//a[@action-type="follow"]')# 找到所有的关注按钮上的 a 标签元素
        
        uid_list=[]
        for a in a_list:
            action_data=a.get_attribute('action-data')# 获取 action-data 属性
            uid=action_data.split('&')[-3].split('=')[1]# 获取uid的值
            uid_list.append(uid)# 将uid加入到list中
        return uid_list # 返回本页所有的uid

    def login_verification_code(self, phone_num, v_code):
        self.driver.get("https://weibo.com/")
        self.driver.find_element_by_class_name("qrcode_phone").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//div[@node-type = 'mobile_box']/input[@name = 'username']").send_keys(phone_num)
        self.driver.find_element_by_xpath("//div[@node-type = 'activation_box']/input[@name = 'password']").send_keys(v_code)
        self.driver.find_elements_by_class_name("W_btn_a")[1].click()

        return self.driver.get_cookies()

    def get_cookies(self, accounts_file_path, level):
        f = open(accounts_file_path, "r")
        db = DBManager()
        wbop_cookie = WeiboOpWithCoocie()
        for line in f:
            line = line.strip()
            match_ob = re.match("([0-9]+)----(.*)", line)
            username = match_ob.group(1)
            password = match_ob.group(2)

            if db.count(username) == 0:
                print("%s %s" % (username, password))
                cookies = self.login(username, password)
                cookies_js = json.dumps(cookies)
                db.insert_account(cookies_js, username, password, level, wbop_cookie.get_uid(cookies))

        db.db_close()

    def update_cookies(self, level):
        wbop = WeiboOpWithCoocie()

        db = DBManager()
        accounts = db.get_accounts(3)
        for account in accounts:
            cookies = json.loads(account[0])
            uid = account[1]
            username = account[2]
            password = account[3]
            while wbop.home(uid, cookies) is False:
                print("%s %s" % (username, password))
                cookies = self.login(username, password)
                
            db.update_cookies(json.dumps(cookies), username)

        db.db_close()

if __name__ == "__main__":

    # op.get_cookie()
    # operator = WBoperator()
    # operator.login("13768336719", "666666777777")
    # operator.delete(1900)
    op = WBoperator()
    op.update_cookies(3)
    # co = op.login("18244808530", "wwweee6981228.")
    # print(co)
    # pickle.dump(co, open("./co_182", "wb"))

    # header = {
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "Accept-Encoding": "gzip,deflate,br",
    #     "Accept-Language": "zh-CN,zh;q=0.8",
    #     "Connection": "keep-alive",
    #     "Host": "weibo.com",
    #     "Referer": "https://weibo.com/",
    #     "Upgrade-Insecure - Requests": "1",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    # }
    # co = pickle.load(open("./co_182", "rb"))
    # cookie = ""
    # for c in co:
    #     cookie = "%s;%s=%s" % (cookie, c["name"], c["value"])
    # header["Cookie"] = cookie[1:]# 去掉首个分号
    # print(json.dumps(co, indent=2))
    #
    # print(requests.get("https://weibo.com/u/6434349828/home", headers=header).text)
#  15151892433,ZSMuYu104104

# operator=WBoperator()
# operator.login('15850782585', 'Weibo6981228.')
#

# for i in range(41)[39:]:
#     page=i+1# 页码
#
#     uid_list_unf=operator.get_followlist_unf('2622535523', page)
#     operator.follow_uidlist(uid_list_unf)
#     print(u'第'+str(page)+u'页关注完毕！')

# operator.delete(2)
# path_list=[]
# for i in range(9):
#     path_list.append('"C:\\Users\\15850\\Documents\\GitHub\\MyWorkspace\\py_study\\img\\'+str(i+1)+'.jpg"')
# 
# upl=Uploader()
# upl.login('15850782585','Weibo6981228.')
# 
# upl.upload_txt(u'测试无图')
# upl.send()
# upl.upload_txt_img(u'测试单图',path_list[0])
# upl.send()
# upl.upload_txt_multiImg(u'测试9图',path_list)
# upl.send()