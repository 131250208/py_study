# -*- coding:utf-8 -*
from selenium import webdriver
from time import sleep
import time
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException

class CourseSelectionSys:

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)# 设置隐性等待时间，等待页面加载完成才会进行下一步，最多等待10秒
    driver.set_window_size(1920, 1080)# 用phantomjs必须有这行

    # 登录并进入到选课界面
    def login(self, usrname, pwd):
        self.driver.get("http://sep.ucas.ac.cn/")

        # 输入账号密码并点击登录
        username = self.driver.find_element_by_id("userName")
        password = self.driver.find_element_by_id("pwd")
        username.send_keys(usrname)
        password.send_keys(pwd)
        print u"请输入验证码"
        self.driver.find_element_by_xpath("//input[@name = 'certCode']").send_keys(input())

        bt_login = self.driver.find_element_by_id("sb")
        bt_login.click()

        # 找到并点击选课系统
        choose_course = self.driver.find_element_by_xpath("//a[@href = '/portal/site/226/821']")
        choose_course.click()

        # 点击【选修课程】-》【选择课程】
        self.driver.execute_script('''$("a:contains('选修课程')").click()''')
        sleep(1)
        self.driver.find_element_by_xpath('//a[@href="/courseManage/main"]').click()
        sleep(1)

    # 监听等待，直到可选
    def listen_choose(self, phone_number, school, course_code, on):
        # 输入移动电话-》点击学院-》点击【新增加本学期研究生课程】
        mobilePhone = self.driver.find_element_by_id("mobilePhone")
        mobilePhone.clear()
        mobilePhone.send_keys(phone_number)
        self.driver.find_element_by_xpath("//label[text() = '"+ school +"']/preceding-sibling::input[1]").click()
        self.driver.find_element_by_xpath("//form[@id = 'regfrm2']/div[7]/button").click()

        # 判断当前表格中是否有目标课程
        try:
            self.driver.find_elements_by_xpath("//td[text() = '" + course_code + "']")
        except NoSuchElementException:
            print u"没有这个课程代号或者该课程已选。"
            return

        while True:
            # 给目标课程的checkbox 加上类名，方便查找元素并获取disabled的属性值
            self.driver.execute_script(
                '''$('td:contains("'''+ course_code + '''")').prev().prev().find("input").addClass("choose_checkbox")''')
            if on == "true":
                self.driver.execute_script('''$('td:contains("'''+ course_code + '''")').prev().find("input").addClass("on_checkbox")''')

            input_choose = self.driver.find_element_by_class_name("choose_checkbox")
            status = input_choose.get_attribute("disabled")
            if status == "true":
                print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + u": " + course_code + u"还未有人退选，持续监控中……"
                self.driver.refresh()
                sleep(1)
            else:
                print course_code + u"监听到可选状态，抢课中！"
                self.click(input_choose)
                if on == "true":
                    self.click(self.driver.find_element_by_class_name("on_checkbox"))
                break

        # 跳出循环，点击【确定提交选课】
        btn_submit = self.driver.find_element_by_xpath("//button[@id = 'cancelBtn']/preceding-sibling::button[1]")
        self.click(btn_submit)

        # 点击【确定】
        self.driver.execute_script('''$("div#jbox-states").find("button[value = 'ok']").click()''')

        # 获取提示信息
        message = self.driver.find_element_by_xpath("//div[@class = 'head']").text
        print message.replace(u"×", "")
        if not u"选课成功" in message and not u"时间冲突" in message:
            print u"选课失败,继续监听..."
            self.listen_choose(phone_number, school, course_code, on)

    # 带屏幕滚动的click
    def click(self, element):
        try:
            element.click()
        except ElementNotVisibleException:
            self.driver.execute_script("window.scrollBy(0,800)")
            sleep(1)
            self.click(element)

if __name__ == "__main__":
    # 从配置文件中读取需要的信息
    print u"读取配置文件中的信息..."
    config = open("config")
    config_dict = {}
    while True:
        line = config.readline()
        if not line:
            break
        else:
            info = line.split(" = ")
            config_dict[info[0]] = info[1].replace("\n", "") # 去除回车

    print u"登录中..."
    css = CourseSelectionSys()
    css.login(config_dict["username"], config_dict["password"])

    print config_dict["username"] + u"已登录，开始监听等待..."

    # 监听等待，直到可选
    css.listen_choose(config_dict["phone_number"], config_dict["school"], config_dict["course_code"], config_dict["on"])

# $('td:contains("201M4006H")').prev().find("input").click();$('td:contains("201M4006H")').prev().prev().find("input").click();$("button#cancelBtn").prev().click();