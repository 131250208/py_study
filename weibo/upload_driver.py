# -*- coding:utf-8 -*-
'''
Created on 2017年6月25日

@author: wycheng
'''
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import os

class Uploader:
    driver = webdriver.Chrome(executable_path='../drivers/chromedriver.exe')# chrome浏览器驱动
    # 根据验证框的存在与否判断是否要输入验证码
    def isVerifyCodeExist(self):
        try:
            self.driver.find_element_by_css_selector('input[name="verifycode"]')
            return True
        except:
            return False
    
    # 输入验证码部分，如果无需输入则直接返回，否则手动输入成功后返回        
    def inputVerifyCode(self):
        input_verifycode=self.driver.find_element_by_css_selector('input[name="verifycode"]')# 验证码输入框
        bt_change=self.driver.find_element_by_css_selector('img[action-type="btn_change_verifycode"]')# 验证码图片，点击切换
        bt_logoin=self.driver.find_element_by_class_name('login_btn')# 登录按钮
        while self.isVerifyCodeExist():
            print u'请输入验证码……(输入"c"切换验证码图片)'
            verifycode=raw_input()
            if verifycode=='c':
                bt_change.click()
            else:
                input_verifycode.send_keys(verifycode)
                bt_logoin.click()
                # 点击完登录以后判断是否成功
                if self.driver.current_url.split('/')[-1]=='home':
                    print u'登录成功'
                    break
                else:
                    print u'输入的验证码不正确'
    
    #打开微博首页进行登录的过程
    def login(self,account,password):
        self.driver.implicitly_wait(10)# 设置隐性等待时间，等待页面加载完成才会进行下一步，最多等待10秒
        url='http://weibo.com/'
        self.driver.get(url)
        #输入账号密码并登录
        WebDriverWait(self.driver,10).until(lambda x:x.find_element_by_xpath('//input[@id="loginname"]')).send_keys(account)
        self.driver.find_element_by_css_selector('input[type="password"]').send_keys(password)
        
        bt_logoin=self.driver.find_element_by_class_name('login_btn')
        bt_logoin.click()
        
        #如果存在验证码，则进入手动输入验证码过程
        if self.isVerifyCodeExist():
            self.inputVerifyCode()  
            
    # 上传文字
    def upload_txt(self,text):
        input_w=self.driver.find_element_by_xpath('//div[@node-type="textElDiv"]/textarea[@class="W_input"]')
        input_w.send_keys(text)
        sleep(1)
    
    #运行上传图片脚步
    def upload_img_script(self,time_bef,time_after,path):# path 需要前后带引号
        sleep(time_bef)# 等待弹窗时间
        os.system('C:/Users/15850/Documents/GitHub/MyWorkspace/py_study/script/upload.exe '+path)
        sleep(time_after)# 等待图片加载时间
    # 上传文字和单图
    def upload_txt_img(self,text,img_path):
        self.upload_txt(text)# 将文字上传
        img=self.driver.find_element_by_css_selector('a[action-type="multiimage"]')
        img.click()
        sleep(1)
        
        bt_uploadimg=WebDriverWait(self.driver,10).until(lambda x:x.find_element_by_xpath('//object[contains(@id,"swf_upbtn")]'))
        bt_uploadimg.click()
        
        self.upload_img_script(1,2,img_path)
    
    # 上传文字和多图    
    def upload_txt_multiImg(self,text,img_path_list):
        self.upload_txt_img(text,img_path_list[0])# 将文字和第一张图片上传
       
        len_imgs=len(img_path_list)    
        bt_uploadimg=WebDriverWait(self.driver,10).until(lambda x:x.find_element_by_xpath('//li[@node-type="uploadBtn"]/div/object[contains(@id,"swf_upbtn")]'))
        for i in range(len_imgs-1):# 将剩余图片 
            bt_uploadimg.click()
            self.upload_img_script(1, 2,img_path_list[i+1])
    
    # 发布
    def send(self):
        self.driver.find_element_by_class_name('W_btn_a').click()
        sleep(4)# 等待发送成功字样消失



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