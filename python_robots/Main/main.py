import requests
import time
import os

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
        # print(url)
        r = self.session.get(url=url, params=params)
        data = r.text.split(';')
        code = data[0].split('=')[1]
        # print(code)
        if code == ' 200' :
            self.uuid =  data[1].split('=',1)[1][2:14]
        else:
            raise Exception('getUUID Failed')

    def getQrcode(self):
        url = BASE_URL + '/qrcode/' + self.uuid
        r = self.session.get(url=url)
        with open('Qrcode.jpg', 'wb') as f:
            f.write(r.content)
        os.startfile('Qrcode.jpg')

    def isLogin(self):
        url = BASE_URL + '/cgi-bin/mmwebwx-bin/login'
        params = {
            '_': int(time.time()),
            'loginicon' : 'true',
            # 'r': '891911636',
            'tip': 0,
            'uuid': self.uuid[:12]
        }
        r = self.session.get(url=url, params=params)
        data = r.text.split('=',2)
        code = data[1][:3]
        if code == '200':
            url = data[2][1:-2] + '&fun=new'
            r = self.session.get(url)
            with open('get.txt', 'wb') as f:
                f.write(r.content)
            print(url)
            return False
        return True

if __name__ == '__main__':
    g = Main()
    g.getUUID()
    g.getQrcode()
    g.isLogin()
    while g.isLogin(): 
        time.sleep(1)
    print ('Done')