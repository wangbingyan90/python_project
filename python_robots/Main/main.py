import requests
import time

BASE_URL = 'https://login.weixin.qq.com'
class Main:
    def __init__(self):
        self.uuid = None
        self.session = requests.Session()

    def getUUID(self):
        url = BASE_URL + '/jslogin'
        params = {
        'appid': 'wx782c26e4c19acffb',
        'fun': 'new',
        'lang': 'zh_CN',
        '_': int(time.time()),
        }
        r = requests.get(url=url, params=params)
        data = r.text.split(';')
        code = data[0].split('=')[1]
        uuid = data[1].split('=',1)[1][2:14]
        print(code)
        print(uuid)
        return uuid

    def getQrcode(self):
        uuid = getUUID()
        url = 'https://login.weixin.qq.com/qrcode/' + uuid
        r = requests.get(url=url)
        with open('Qrcode.jpg', 'wb') as f:
            f.write(r.content)
        print(url)

    def isLogin(self,uuid):
        url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login'
        params = {
            '_': int(time.time()),
            'loginicon' : 'true',
            'r': '891911636',
            'tip': 0,
            'uuid':uuid[:12]
        }