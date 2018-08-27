import requests,time,os,re,json
from SyncMsg import SyncThread
import Static,Log,SqlLitUtil

BASE_URL = 'https://login.weixin.qq.com'

class WeChatLogin:

    def __init__(self):
        self.uuid = None
        self.userName = None
        self.jsonHeaders = {'ContentType': 'application/json; charset=UTF-8'}
        self.session = requests.Session()
        self.loginInfo = {}
        self.sql = SqlLitUtil.SqlLitUtil()


    def doLogin(self):
        while self.getUUID():
            time.sleep(1)
        self.getQrcode()
        while self.isLogin():
            time.sleep(1)
        self.webInit()
        self.doWebwxstatusnotify()
        self.getContract()
        Log.log(Static.I,'登陆成功')
        print('登陆成功，进行同步数据')
        syncThread = SyncThread(self.session,self.loginInfo)
        syncThread.start()
        # while self.doSynccheck():
        #     time.sleep(5)

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
            Log.log(Static.I,'UUID获取成功')
            return False
        else:
            print('getUUID Failed')
            Log.log(Static.E,'UUID获取失败')
            return True


    def getQrcode(self):
        url = BASE_URL + '/qrcode/' + self.uuid
        r = self.session.get(url=url)
        with open('Qrcode.jpg', 'wb') as f:
            f.write(r.content)
        Log.log(Static.I,'二维码获取成功')
        try:
            os.startfile('Qrcode.jpg')
            Log.log(Static.I,'二维码打开成功')
        except:
            Log.log(Static.E,'二维码打开失败，使用打印二维码')
            from ShowQRCode import ShowQrcode
            ShowQrcode('Qrcode.jpg', 37, 3).print_qr()


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
            self.loginInfo['url'] = data[2][1:-2]
            r = self.session.get(self.loginInfo['url'], allow_redirects=False)
            self.loginInfo['url'] = self.loginInfo['url'][:self.loginInfo['url'].rfind('/')]
            # print(self.loginInfo['url'])
            self.setLoginInfo(r.text)
            Log.log(Static.I,'确认登录')
            return False
        if code == '201':
            Log.log(Static.I,'完成扫描')
            print("扫描成功，等待确认")
        return True


    def setLoginInfo(self, xmldata):   
        self.loginInfo['BaseRequest'] = {}                                                
        data = re.findall(r'>(.*?)<',xmldata)
        self.loginInfo['BaseRequest']['Skey'] = data[5]
        self.loginInfo['BaseRequest']['Sid'] = data[7]
        self.loginInfo['BaseRequest']['Uin'] = data[9]
        self.loginInfo['BaseRequest']['DeviceID'] = data[11]


    # 初始化进入界面数据
    def webInit(self):
        url = self.loginInfo['url'] + '/webwxinit?r= ' + str(int(time.time()))
        params = {
            'BaseRequest': self.loginInfo['BaseRequest']
        }
        r = self.session.post(url, data = json.dumps(params), headers = self.jsonHeaders)
        r.encoding = r.apparent_encoding
        # print(r.text)
        dic = json.loads(r.text)
        self.loginInfo['SyncKey'] = dic['SyncKey']
        self.loginInfo['synckey'] = '|'.join([str(item['Key'])+'_'+str(item['Val']) for item in dic['SyncKey']['List']])
        # print(self.loginInfo['synckey'])
        self.userName = dic['User']['UserName']
        Log.log(Static.I,'初始化界面')


    # 开启微信状态通知
    def doWebwxstatusnotify(self):
        url = self.loginInfo['url'] + '/webwxstatusnotify'
        params = {
                'BaseRequest': self.loginInfo['BaseRequest'],
                'Code': 3,
                'FromUserName': self.userName,
                'ToUserName': self.userName,
                'ClientMsgId': int(time.time()),
                }
        r = self.session.post(url, data = json.dumps(params), headers = self.jsonHeaders)
        Log.log(Static.I,'开启微信状态通知')


    # 获取联系人
    def getContract(self):
        url = self.loginInfo['url'] + '/webwxgetcontact'
        params = {
            'r': int(time.time()),
            'seq': 0,
            'skey': self.loginInfo['BaseRequest']['Skey'],
        }
        r = self.session.get(url, params=params,headers = self.jsonHeaders)
        r.encoding = r.apparent_encoding
        data = json.loads(r.text)['MemberList']
        self.sql.addContracts(data)


    # 同步刷新
    def doSynccheck(self):
        url = self.loginInfo['url'] + '/synccheck'
        params = {
            'r': int(time.time()),
            'skey': self.loginInfo['BaseRequest']['Skey'],
            'sid': self.loginInfo['BaseRequest']['Sid'],
            'uin': self.loginInfo['BaseRequest']['Uin'],
            'deviceid': self.loginInfo['BaseRequest']['DeviceID'],
            'synckey': self.loginInfo['synckey'],
        }
        r = self.session.get(url, params = params)
        print(r.text)
        data = r.text.split(':')
        if data[1][1:2] == '0':
            print('更新')
            if data[2][1:2] == '0':
                print('没有新消息')
                return True
            else:
                msgList = self.getNewMsg()
                if msgList:
                    self.printMsg(msgList)
                else:
                    print('信息数量：0')
                return True
        print('退出登录')
        return False


    # 获取新信息
    def getNewMsg(self):
        url = self.loginInfo['url'] + '/webwxsync?sid=' + self.loginInfo['BaseRequest']['Sid'] + '&skey=' + self.loginInfo['BaseRequest']['Skey'] + '&pass_ticket=' + self.loginInfo['BaseRequest']['DeviceID'] 
        params = {
            'BaseRequest': self.loginInfo['BaseRequest'],
            'SyncKey': self.loginInfo['SyncKey'],
            'rr': ~int(time.time())
        }
        print(params)
        r = self.session.post(url, data = json.dumps(params),headers = self.jsonHeaders)
        r.encoding = r.apparent_encoding
        dic = json.loads(r.text)
        print(dic)
        self.loginInfo['SyncKey'] = dic['SyncKey']
        self.loginInfo['synckey'] = '|'.join([str(item['Key'])+'_'+str(item['Val']) for item in dic['SyncKey']['List']])
        if dic['AddMsgCount'] != 0: return dic['AddMsgList']
        return None


    def printMsg(self,msgList):
        for m in msgList:
            print(m['FromUserName'])
            print(m['Content'])
        
    def sendMsg(self,toUserName='filehelper', msg = 'Test Message'):
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
        print('发送完成')


if __name__ == '__main__':
    g = WeChatLogin()
    g.doLogin()
    g.sendMsg()
    time.sleep(10)
    g.sendMsg()
    time.sleep(10)
    print ('Done')