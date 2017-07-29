# -*- coding:utf8 -*-

from selenium import webdriver
import time

class BaiduOperator:
    
    # driver = webdriver.PhantomJS(service_args=['--remote-debugger-port=9001'])
    driver = webdriver.Chrome()
    driver.viewportSize = {'width': 1024, 'height': 800}  # 重要这句！
    driver.maximize_window()
    driver.implicitly_wait(10)  # 设置隐性等待时间，等待页面加载完成才会进行下一步，最多等待10秒

    # 尝试是否登录成功，成功则返回username
    def try_logined(self):
        try:
            span_username = self.driver.find_element_by_class_name("user-name")
        except:
            return None
        else:
            return span_username.text

    # 登录操作
    def login(self,username,pswd):
        url_baiduyun = "https://pan.baidu.com/"
        self.driver.get(url_baiduyun)
        self.driver.find_element_by_xpath(
            "//div[@class='header-login']/div[@class='pass-login-tab']/div[@class='account-title']").click()

        inp_username = self.driver.find_element_by_xpath("//input[contains(@id,'userName')]")
        inp_pswd = self.driver.find_element_by_xpath("//input[contains(@id,'password')]")
        inp_submit = self.driver.find_element_by_xpath("//input[contains(@id,'submit')]")

        inp_username.send_keys(username)
        inp_pswd.send_keys(pswd)
        # self.driver.save_screenshot("../img/phantomjs.jpg")
        inp_submit.click()

    # 对资源进行转存
    def transfer(self,url_resrc):
        self.driver.get(url_resrc)



        # 尝试找全选按钮,找不到说明是单个文件
        try:
            check_all = self.driver.find_element_by_class_name("zbyDdwb")
        except:
            print u"找不到对应元素"
        else:
            check_all.click()
        # 进行转存

        time.sleep(1)
        btn_save = self.driver.find_element_by_xpath("//div[@class='bar']/div[@class='button-box']/a[@data-button-id='b1']")
        print btn_save.text

        self.driver.execute_script("arguments[0].click();", btn_save)

        time.sleep(5)
        # path = self.driver.find_element_by_xpath("//span[@node-path = '/电影']")
        # path.click()
        #
        # btn_right = self.driver.find_element_by_class_name("g-button-right")
        # btn_right.click()
        #
        # # 检验是否成功保存
        # tip_info = self.driver.find_element_by_class_name("tip-msg").text
        # if "已为您成功保存文件" in tip_info:
        #     print "transfer succeed!"
        # else:
        #     print "transfer fail..."

baiduoperator = BaiduOperator()
baiduoperator.login("504757794@qq.com","wwweee6981228.")
username_logined = baiduoperator.try_logined()

if username_logined == None:
    print "login fail"
else:
    print "login successfully! username: " + username_logined
    baiduoperator.transfer("http://pan.baidu.com/s/1i5GGqCP#list/path=%2F")


