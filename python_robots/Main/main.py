import requests
import time
import os
import re
import json

BASE_URL = 'https://login.weixin.qq.com'
class Main:

    def __init__(self):
        self.uuid = None
        self.userName = None
        self.jsonHeaders = {'ContentType': 'application/json; charset=UTF-8'}
        self.session = requests.Session()
        self.loginInfo = {}
        self.doLogin()



    def doLogin(self):
        while self.getUUID():
            time.sleep(1)
        self.getQrcode()
        while self.isLogin():
            time.sleep(1)
        self.webInit()
        # self.getContract()

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
            return False
        else:
            print('getUUID Failed')
            return True


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
            # url = data[2][1:-2] + '&fun=new'
            # r = self.session.get(url)
            # with open('get.txt', 'wb') as f:
            #     f.write(r.content)
            self.loginInfo['url'] = data[2][1:-2]
            r = self.session.get(self.loginInfo['url'], allow_redirects=False)
            self.loginInfo['url'] = self.loginInfo['url'][:self.loginInfo['url'].rfind('/')]
            # print(self.loginInfo['url'])
            self.setLoginInfo(r.text)
            return False
        return True


    def setLoginInfo(self, xmldata):   
        self.loginInfo['BaseRequest'] = {}                                                
        data = re.findall(r'>(.*?)<',xmldata)
        self.loginInfo['BaseRequest']['Skey'] = data[5]
        self.loginInfo['BaseRequest']['Sid'] = data[7]
        self.loginInfo['BaseRequest']['Uin'] = data[9]
        self.loginInfo['BaseRequest']['DeviceID'] = data[11]


    def webInit(self):
        url = self.loginInfo['url'] + '/webwxinit?r= ' + str(int(time.time()))
        params = {
            'BaseRequest': self.loginInfo['BaseRequest']
        }
        r = self.session.post(url, data = json.dumps(params), headers = self.jsonHeaders)
        r.encoding = r.apparent_encoding
        dic = json.loads(r.text)
        print(r.text)
        self.userName = dic['User']['UserName']
        print(dic['ContactList'][2]['NickName'])
        self.sendMsg(dic['ContactList'][2]['UserName'])
        print(self.userName)

    # 获取联系人
    def getContract(self):
        url = self.loginInfo['url'] + '/webwxgetcontact'
        params = {
            'r': int(time.time()),
            'seq': 0,
            'skey': self.loginInfo['BaseRequest']['Skey'],
        }
        r = self.session.get(url=url, params=params,headers = self.jsonHeaders)
        r.encoding = r.apparent_encoding
        data = json.loads(r.text)['MemberList']


    def sendMsg(self,toUserName, msg = 'Test Message'):
        url = self.loginInfo['url'] + '/webwxsendmsg'
        params = {
            'BaseRequest': self.loginInfo['BaseRequest'],
            'Msg': {
                'Type': 1,
                'Content': msg,
                'FromUserName': self.userName,
                'ToUserName': toUserName,
                'LocalID': str(int(time.time())),
                'ClientMsgId': str(int(time.time())),
                },
        }
        r = self.session.post(url=url, data = json.dumps(params),headers = self.jsonHeaders)
        r.encoding = r.apparent_encoding
        print(r.text)


if __name__ == '__main__':
    g = Main()
    # g.sendMsg('@ab195e9b1cb0c30cabfa2bb3e748e268')
    print ('Done')