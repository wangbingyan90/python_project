import threading,time,json
import Static,Log


class SyncThread (threading.Thread):

    def __init__(self,session,loginInfo):
        threading.Thread.__init__(self)
        self.session = session
        self.loginInfo = loginInfo
        self.jsonHeaders = {'ContentType': 'application/json; charset=UTF-8'}
    

    def run(self):
        Log.log(Static.I,'同步数据')
        while self.doSynccheck():
            time.sleep(3)


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
            Log.log(Static.I,'进行更新')
            print('进行更新')
            if data[2][1:2] == '0':
                Log.log(Static.I,'没有新消息')
                print('没有新消息')
                return True
            else:
                msgList = self.getNewMsg()
                if msgList:
                    self.printMsg(msgList)
                else:
                    Log.log(Static.I,'信息数量：0')
                    print('信息数量：0')
                return True
        print('退出登录')
        Log.log(Static.I,'退出登录')
        return False


    # 获取新信息
    def getNewMsg(self):
        url = self.loginInfo['url'] + '/webwxsync?sid=' + self.loginInfo['BaseRequest']['Sid'] + '&skey=' + self.loginInfo['BaseRequest']['Skey'] + '&pass_ticket=' + self.loginInfo['BaseRequest']['DeviceID'] 
        params = {
            'BaseRequest': self.loginInfo['BaseRequest'],
            'SyncKey': self.loginInfo['SyncKey'],
            'rr': ~int(time.time())
        }
        r = self.session.post(url, data = json.dumps(params),headers = self.jsonHeaders)
        r.encoding = r.apparent_encoding
        dic = json.loads(r.text)
        # print(dic)
        self.loginInfo['SyncKey'] = dic['SyncKey']
        self.loginInfo['synckey'] = '|'.join([str(item['Key'])+'_'+str(item['Val']) for item in dic['SyncKey']['List']])
        if dic['AddMsgCount'] != 0: return dic['AddMsgList']
        return None


    def printMsg(self,msgList):
        for m in msgList:
            print(m['FromUserName'])
            print(m['Content'])