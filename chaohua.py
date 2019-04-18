# author: cw1997
# 2019-04-18 20:06:30
# repo: https://github.com/cw1997/chaohua-sign

import json
import urllib
import re

import requests
import pprint

# config
username = "867597730@qq.com"
password = ""
chaohua_list = ['bug', '台湾']


headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Origin': 'https://passport.weibo.cn', 'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}


# login weibo.cn wap
def weibo_login(session, username, password):
    login_api = "https://passport.weibo.cn/sso/login"
    data = {'username': username, 'password': password, 'savestate': '1', 'entry': 'mweibo'}
    r = session.post(login_api, data=data, headers=headers)
    print(r.text)
    ret_json = json.loads(r.text)
    # print(ret_json)
    # sso login all domain(weibo.com and sina.com.cn)
    crossdomainlist = ret_json['data']['crossdomainlist']
    for i in crossdomainlist:
        v = crossdomainlist[i]
        print(i, v)
        r = session.get(v, headers=headers)
        print(r.text)

def get_chaohua_id(session, chaohua_name):
    r = session.get('https://s.weibo.com/related?q='+chaohua_name, headers=headers)
    text = r.text
    # pprint.pprint(text)
    ret = re.findall('<a href="\/\/weibo\.com\/p\/(.*?)" target="_blank"', text)
    # pprint.pprint(ret)
    for chaohua_id in ret:
        if chaohua_id[0:4] == "1008":
            return chaohua_id

# print(get_chaohua_id("bug"))
# exit()

def sign_chaohua(session, chaohua_id):
    sign_api = "https://weibo.com/p/aj/general/button?ajwvr=6&api=http://i.huati.weibo.com/aj/super/checkin&texta=%E7%AD%BE%E5%88%B0&textb=%E5%B7%B2%E7%AD%BE%E5%88%B0&status=0&id="+chaohua_id+"&location=page_100808_super_index&__rnd=1555588260458"
    r = session.get(sign_api, headers=headers)
    print(r.text)
    return r.text

if __name__ == '__main__':
    session = requests.Session()
    weibo_login(session, username, password)
    for chaohua_name in chaohua_list:
        chaohua_id = get_chaohua_id(session, chaohua_name)
        print(chaohua_name, chaohua_id, 'start sign')
        ret = sign_chaohua(session, chaohua_id)
        ret_json = json.loads(ret)
        print(chaohua_name, ret_json['msg'], 'sign end')


