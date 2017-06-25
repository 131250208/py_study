# -*- coding:utf-8 -*-
'''
Created on 2017年6月19日

@author: wycheng
'''

import requests
import json
import urllib

# url_authorize='https://api.weibo.com/oauth2/authorize?client_id=4258807233&response_type=code&redirect_uri=https://api.weibo.com/oauth2/default.html'

# url='https://api.weibo.com/oauth2/access_token'
# param={'client_id':'4258807233',
#        'client_secret':'94862954431d434124903514fc4d07bf',
#        'grant_type':'authorization_code',
#        'redirect_uri':'https://api.weibo.com/oauth2/default.html',
#        'code':'4dcec989fd8574f649703050c4dbfb5a'
#        }
# response=requests.post(url,param)
# print response.text
# ob_json=json.loads(response.text)

url_upload='https://api.weibo.com/2/statuses/update.json'
text=u'测试文本1'
# text_encoded=urllib.quote(text)
param={'access_token':'2.00fk4vmGP_WNeE9564959dfbsrJuvD',
#        'visible':'1',
#        'url':'http://upload-images.jianshu.io/upload_images/4355294-1f5291a869103554.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240',
       'status':text}
 
response=requests.post(url_upload, param)
print response.text
# param = urllib.urlencode(param)