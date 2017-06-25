# -*- coding:utf-8 -*-
'''
Created on 2017年6月22日

@author: 15850
'''
from snspy import APIClient
from snspy import SinaWeiboMixin     

APP_KEY = '4258807233'            # app key
APP_SECRET = '94862954431d434124903514fc4d07bf'      # app secret
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'  # callback url
YOUR_ACCESS_TOKEN='2.00fk4vmGP_WNeE9564959dfbsrJuvD'
EXPIRES_TIME='1655807629'

client = APIClient(SinaWeiboMixin, app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL,
                     access_token=YOUR_ACCESS_TOKEN, expires=EXPIRES_TIME)
# url = client.get_authorize_url()
# print url

# r = client.request_access_token('6adcf15ac7d789bbaff52fe4a80578d6')
# access_token = r.access_token  # access token 2.00fk4vmGP_WNeE9564959dfbsrJuvD
# expires = r.expires # 1655807629

# print client.statuses.update.post(status=u'再测试一条')
# print client.statuses.upload.post(status=u'测试一下发图片',
#                                   pic=open('C:/Users/15850/Desktop/120.jpg'))