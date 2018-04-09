# coding:utf-8
#
# 爬虫并回复
# 添加关注事件
#
from hashlib import sha1
from flask import Flask, request
import requests
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

token = 'wby520'


app = Flask(__name__)


def get_update(token, timestamp, nonce):
    arguments = ''
    for k in sorted([token, timestamp, nonce]):
        arguments = arguments + str(k)
    m = sha1()
    m.update(arguments.encode('utf8'))
    return m.hexdigest()


def check_signature():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    check = get_update(token, timestamp, nonce)
    return True if check == signature else False


def parse_xml(data):
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
    root = ET.fromstring(data)
    server = root.find("ToUserName").text
    user = root.find("FromUserName").text
    type = root.find("MsgType").text
    # content = root.find("Content").text
    content = 'unknow'
    return server, user, type, content


def captureData():
    headers = {
        'Host': "www.520yb.top",
        'Connection': "keep-alive",
        'Accept': "application/json",
        'X-Requested-With': "XMLHttpRequest",
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0.1; C106 Build/ZAXCNFN5801712291S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/49.0.2623.91 Mobile Safari/537.36 Html5Plus/1.0",
        'Content-Type': "application/json",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,en-US;q=0.8"
    }
    r = requests.get('http://43.225.157.231/api/values/GetShort',
                     headers=headers, timeout=30).text
    s = r[30:3000]
    hrefs = re.findall(r'shorturl\":\"(.*?)\"', s)
    url = '链接:\n'
    for one in hrefs:
        url = url + 'https://pan.baidu.com/mbox/homepage?short=' + one + '\n'
    return url


def dealMsg(type, content):
    if type == 'event':
        return '欢迎关注wecat1.1，回复仍以内容即可获得链接\n' + captureData()
    return captureData()


def createMsg(server, user, type, content):
    template = """
    <xml>
		<ToUserName><![CDATA[{}]]></ToUserName>
        <FromUserName><![CDATA[{}]]></FromUserName>
        <CreateTime>{}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{}]]></Content>
    </xml>
    """
    result = template.format(user, server, int(time.time()), content)
    return result


@app.route('/weixin', methods=['GET', 'POST'])
def weixinInterface():
    if request.method == 'GET':
        print '进行验证'
        if check_signature:
            print '验证成功'
            echostr = request.args.get('echostr', '')
            return echostr
        else:
            print '验证失败'
            return 'signature error'
    else:
        data = request.data
        server, user, type, content = parse_xml(data)
        msg = createMsg(server, user, type, dealMsg(type, content))
        return msg


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
