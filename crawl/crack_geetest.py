# -*- coding:utf-8 -*-
'''
Created on 2017年6月15日

@author: wycheng
'''
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from PIL import Image
import StringIO
import random
from linecache import getlines

'''
该函数用于截图并保存到指定地址
'''
def get_screenshot(filename):
    screenshot=driver.get_screenshot_as_png()
    screenshot = Image.open(StringIO.StringIO(screenshot))
    captcha = screenshot.crop((450, 222, 780, 396))
    captcha.save(filename)
    return captcha
    
'''
该函数用于比较某一列像素点是否相同，为了忽略掉浅印，允许一定程度的容差
'''
def isequal_col(j,img1,img2,tolerance):# j: j列的像素点，img: 图片对象，tolerance: 容差
    height=img1.size[1]
    pix1=img1.load()
    pix2=img2.load()
    
    for i in range(height):
        rgb1=pix1[j,i]
        rgb2=pix2[j,i]
        if abs(rgb1[0]-rgb2[0])>tolerance or abs(rgb1[1]-rgb2[1])>tolerance or abs(rgb1[2]-rgb2[2])>tolerance:
            return False
    return True

def getLines(img1,img2,tolerance):
    #获取几条边界线的y坐标
    lines=[]
    flag=False
    width=img1.size[0]
    for j in range(width):
        if isequal_col(j, img1, img2, tolerance)==flag:
            lines.append(j)
            flag=not flag
    
    return lines

def getOffset(img1,img2,tolerance):
    lines=getLines(img1,img2,tolerance)
    #根据lines的长度情况计算并返回位移
    if len(lines)==4:
        return lines[3]-lines[1]
    elif len(lines)==2:
        return lines[1]-66
    else:# 如果不是以上两种情况，即容错值不合适，继续调整容差值再算一遍
        return getOffset(img1, img2, tolerance-5)

url = 'https://www.jianshu.com/sign_in'
driver = webdriver.Chrome('../drivers/chromedriver')
driver.get(url)
time.sleep(3)
 
slider_knob=driver.find_element_by_class_name('gt_slider_knob')
actions=ActionChains(driver)
actions.move_to_element(slider_knob).perform()
time.sleep(1)
img1=get_screenshot('../screenshots/before.png')
  
actions.click_and_hold(slider_knob).perform()
time.sleep(3.5)
img2=get_screenshot('../screenshots/after.png')

offset=getOffset(img1, img2, 65)*260/328
print offset

interval=0.5
times=int(4.5/interval)-1
offset_p=offset/times

num=1
offset_current=0
while offset!=0:
    random.seed()
    yoffset=random.randint(0,5)
    xoffset=random.randint(offset_p,offset_p+5)
    if xoffset>offset:
        xoffset=offset
    offset-=xoffset
    actions.move_by_offset(xoffset, yoffset).perform()
    time.sleep(0.5)
    
    print 
    img3=get_screenshot('../screenshots/step'+str(num)+'.png')
    num+=1
    lines1=getLines(img1,img2,60)
    lines2=getLines(img1, img3, 60)
    offset_pra=lines2[0]-lines1[0]
    offset_current+=xoffset
    print u'计划移动',offset_current,u'-----实际移动了',offset_pra,u'----比例',((offset_current+0.)/offset_pra)
    
actions.release(slider_knob).perform()
