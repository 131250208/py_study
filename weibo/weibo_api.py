# -*- coding:utf-8 -*-
'''
Created on 2017年6月19日
此类用来封装微博开放平台的api
@author: wycheng
'''

import requests
import json
import urllib

# 用于获取code，获取的code是一次性的，下次需要code需要再次访问以下链接
# https://api.weibo.com/oauth2/authorize?client_id=4258807233&response_type=code&redirect_uri=https://api.weibo.com/oauth2/default.html

access_token='2.00fk4vmGP_WNeE9564959dfbsrJuvD'

def getAccess_token(code):
    url='https://api.weibo.com/oauth2/access_token'
    param={'client_id':'4258807233',
           'client_secret':'94862954431d434124903514fc4d07bf',
           'grant_type':'authorization_code',
           'redirect_uri':'https://api.weibo.com/oauth2/default.html',
           'code':code
           }
    response=requests.post(url,param)
    print 'weibo_api.getAccess_token:'+response.text
    jsob=json.loads(response.text)
    return jsob['access_token']
    

#print getAccess_token('2acaac487ee3a9a9548e464a288d0f49')# 2.00fk4vmGP_WNeE9564959dfbsrJuvD

# 获取两个用户之间的关系
def getFriendship(uid_source,uid_target):
    url='https://api.weibo.com/2/friendships/show.json'
    param={'access_token':access_token,
           'source_id':uid_source,
           'target_id':uid_target}
    response=requests.get(url,param)
    print 'weibo_api.getFriendship:'+response.text
    jsob=json.loads(response.text)
    
    if 'error' in jsob:
        return 'api error'
    elif 'source' in jsob:
        followed_by=jsob['source']['followed_by']
        following=jsob['source']['following']
        
        if not following and not followed_by:
            return '0:0'# 互相不关注
        elif following and not followed_by:
            return '1:0'# 已关注，未被关注
        elif not following and followed_by:
            return '0:1'# 未关注，已被关注
        elif following and followed_by:
            return '1:1'# 互相关注
    
# 通过用户昵称查id
def getID(username):# 返回的是str类型
    url='https://api.weibo.com/2/users/show.json'
    param={'access_token':access_token,
           'screen_name':username}
    response=requests.get(url,param)
    print 'weibo_api.getID:'+response.text
    jsob=json.loads(response.text)
    return jsob['idstr']

# 通过id找用户昵称
def getUserName(uid):
    url='https://api.weibo.com/2/users/show.json'
    param={'access_token':access_token,
           'uid':uid}
    response=requests.get(url,param)
    print 'weibo_api.getUserName:'+response.text
    jsob=json.loads(response.text)
    return jsob['screen_name']

# url_upload='https://api.weibo.com/2/statuses/update.json'
# text=u'测试文本1'
# # text_encoded=urllib.quote(text)
# param={'access_token':'2.00fk4vmGP_WNeE9564959dfbsrJuvD',
# #        'visible':'1',
# #        'url':'http://upload-images.jianshu.io/upload_images/4355294-1f5291a869103554.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240',
#        'status':text}
#  
# response=requests.post(url_upload, param)
# print response.text
# # param = urllib.urlencode(param)