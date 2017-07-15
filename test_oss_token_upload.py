#!/usr/bin/env python
# encoding: utf-8

"""
@author: david
@time: 7/14/17 7:31 PM
"""
import web
import MySQLdb

render = web.template.render('templates/')
import oss2
import time
import datetime
import json
import base64
import hmac
from hashlib import sha1 as sha

accessKeyId = '6MKOqxGiGU4AUk44'
accessKeySecret = 'ufu7nS8kS59awNihtjSonMETLI0KLy'
host = 'http://post-test.oss-cn-hangzhou.aliyuncs.com'
expire_time = 30
upload_dir = 'user-dir/'


def get_iso_8601(expire):
    print expire
    gmt = datetime.datetime.fromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt


def get_token(dir_name=upload_dir):
    now = int(time.time())
    expire_syncpoint = now + expire_time
    expire = get_iso_8601(expire_syncpoint)

    policy_dict = {}
    policy_dict['expiration'] = expire
    condition_array = []
    array_item = []
    array_item.append('starts-with')
    array_item.append('$key')
    array_item.append(upload_dir)
    condition_array.append(array_item)
    policy_dict['conditions'] = condition_array
    policy = json.dumps(policy_dict).strip()
    # policy_encode = base64.encodestring(policy)
    policy_encode = base64.b64encode(policy)
    print policy_encode
    h = hmac.new(accessKeySecret, policy_encode, sha)
    sign_result = base64.encodestring(h.digest()).strip()

    token_dict = {}
    token_dict['accessid'] = accessKeyId
    token_dict['host'] = host
    token_dict['policy'] = policy_encode
    token_dict['signature'] = sign_result
    token_dict['expire'] = expire_syncpoint
    token_dict['dir'] = upload_dir
    web.header("Access-Control-Allow-Methods", "POST")
    web.header("Access-Control-Allow-Origin", "*")
    # web.header('Content-Type', 'text/html; charset=UTF-8')
    result = json.dumps(token_dict)
    return result


urls = (
    '/testoss', 'testoss',
    '/token', 'token',
    '/todo', 'todo',
    '/add', 'add',
    # '/(.*)', 'index',
)
app = web.application(urls, globals())


class testoss:
    def GET(self):
        info = render.testoss()
        return info


class add:
    def POST(self):
        i = web.input()
        if hasattr(web, 'insert'):
            n = web.insert('todo', title=i.title)
        else:
            db.insert('todo', title=i.title)
        web.seeother('/todo')


class todo:
    def GET(self):
        if hasattr(web, 'select'):
            todos = web.select('todo')
        else:
            todos = db.select('todo')
        return render.todo(todos)


class index:
    def GET(self, name='Bob'):
        info = render.index(name)
        return info


class token:
    def GET(self, name=upload_dir):
        token = get_token(name)
        print token
        return token


web.config.db_parameters = dict(
    dbn='mysql',
    user='tokenuser',
    pw='123456%$',
    db='token'
)

db = web.database(**web.config.db_parameters)
# db = web.database(
#     dbn='mysql',
#     user='tokenuser',
#     pw='123456%$',
#     db='token',
# )

if __name__ == "__main__":
    app.run()
