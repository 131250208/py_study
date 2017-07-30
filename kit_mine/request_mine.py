# -*- coding:utf-8 -*-
'''
Created on 2017年6月30日

@author: wycheng
'''
import random
import requests
import time
from bs4 import BeautifulSoup
import pickle

class IPs_Agents_Pool:
    iplist = None
    count_used = 0
    count_fail = 0
    count_fail_max = 0
    user_agent_list =None

    def __init__(self,count_max_fail = 5):
        # 初始化代理ip
        self.iplist = pickle.load(open("ips_file.txt","rb"))
        if len(self.iplist) == 0 :
            self.iplist = self.get_save_IPs()

        # 设置允许失败的最大次数
        self.count_fail_max = count_max_fail

        # 可用于切换的user_agent
        self.user_agent_list = [
            # 我的计算机上的浏览器
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
            # chrome
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",  # 火狐
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
            # ie
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
            # 搜狗
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.3.1000 Chrome/39.0.2146.0 Safari/537.36",
            # 遨游云

            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
    def get_save_IPs(self):
        ips_list = []
        url_proxy = 'http://www.iphai.com/free/ng'
        
        print u'正在连接到代理ip网站……'
        response = requests.get(url_proxy)
        
        html_txt = response.text
        soup = BeautifulSoup(html_txt,'lxml')
        
        ip_lines = soup.find('table').find_all('tr')
        for ipline in ip_lines[1:]:# 用切片切掉第一行标题行
            tds = ipline.find_all('td')
            ip,port,res_time = tds[0].text.strip(),tds[1].text.strip(),tds[-2].text.strip()[:-1]# 切片切掉时间的单位's'
            
            if float(res_time) < 5:# 延迟超过5秒的不收入list
                ips_list.append(ip + ':' + port)

        ips_file = open("ips_file.txt", "wb")
        pickle.dump(ips_list, ips_file)

        print u'获取到有效ip:' + str(len(ips_list)) + u"个"
        return ips_list

    # 取得一个代理
    def getIP(self):
        if self.count_fail > self.count_fail_max:
            self.iplist = self.get_save_IPs()
        else:
            len_list = len(self.iplist)
            proxy = self.iplist[self.count_used/len_list]
            self.count_used += 1
            return proxy

    # 取得一个user-agent
    def getAgent(self):
        time_current = time.time()
        random.seed(time_current)
        return random.choice(self.user_agent_list)

    def fail(self):
        self.count_fail += 1

#     def get(self,url,proxies = None,num_retries = 6,timeout = 5):
#         time_current = time.time()
#         random.seed(time_current)
#
#         user_agent = random.choice(self.user_agent_list)
#         headers = {'User-Agent':user_agent}
# #         print u'选中useragent:'+user_agent
#
#         if proxies == None:# 没有代理时，用本机ip
#             try:
#                 response = requests.get(url, headers = headers , timeout = timeout)
# #                 print u'没有使用代理'
#                 return response
#             except:# 一旦本机ip失效，就启用代理ip连接
#                 proxy = random.choice(self.iplist)
# #                 print u'选中proxy：' + proxy
#                 proxies = {'http' : proxy}
#                 return self.get(url, proxies = proxies)
#         else:
#             try:
#                 response = requests.get(url, headers = headers,proxies = proxies,timeout = timeout)
#                 num_retries = 6;# 代理ip连接成功一次就重置重试次数为6
#                 return response
#             except:
#                 if num_retries > 0:# 允许代理最多有5次失效机会
#                     return self.get(url, proxies, num_retries - 1)
#                 else:# 代理连续6次失败后，重新爬取代理ip，再从本机ip开始爬取
#                     self.iplist = self.get_save_IPs()
#                     return self.get(url)
