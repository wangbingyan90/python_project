#!/usr/bin/env python
#coding: utf-8

#
#1，守护进程下的 爬虫回复
#2，关注事件 自动回复
#
import sys, os
from hashlib import sha1
from flask import Flask, request
import requests
import re
import time
reload(sys)
sys.setdefaultencoding('utf8')

'''将当前进程fork为一个守护进程
   注意：如果你的守护进程是由inetd启动的，不要这样做！inetd完成了
   所有需要做的事情，包括重定向标准文件描述符，需要做的事情只有chdir()和umask()了
'''
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
#	content = root.find("Content").text
	content = 'unknow'
	return server,user,type,content

def captureData():
	headers = {
		'Host': "www.520yb.top",
		'Connection':"keep-alive",
		'Accept':"application/json",
		'X-Requested-With':"XMLHttpRequest",
		'User-Agent':"Mozilla/5.0 (Linux; Android 6.0.1; C106 Build/ZAXCNFN5801712291S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/49.0.2623.91 Mobile Safari/537.36 Html5Plus/1.0",
		'Content-Type':"application/json",
		'Accept-Encoding':"gzip, deflate",
		'Accept-Language':"zh-CN,en-US;q=0.8"
		}
	r = requests.get('http://43.225.157.231/api/values/GetShort',headers=headers,timeout=30).text
	s = r[30:3000]
	hrefs = re.findall(r'shorturl\":\"(.*?)\"',s)
	url = '链接:\n'
	for one in hrefs:
		url = url + 'https://pan.baidu.com/mbox/homepage?short=' + one +'\n'
	return url

def dealMsg(type,content):
	if type == 'event':
		return '欢迎关注wechat1.2，回复仍以内容即可获得链接\n' + captureData()
	return captureData()


def createMsg(server,user,type,content):
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
		server,user,type,content = parse_xml(data)
		msg = createMsg(server,user,type,dealMsg(type,content))
		return msg

def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
     #重定向标准文件描述符（默认情况下定向到/dev/null）
    try:
        pid = os.fork()
          #父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。
        if pid > 0:
            sys.exit(0)   #父进程退出
    except OSError, e:
        sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

     #从母体环境脱离
    os.chdir("/")  #chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录
    os.umask(0)    #调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。
    os.setsid()    #setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。

     #执行第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)   #第二个父进程退出
    except OSError, e:
        sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

     #进程已经是守护进程了，重定向标准文件描述符

    for f in sys.stdout, sys.stderr: f.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())    #dup2函数原子化关闭和复制文件描述符
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

#示例函数：每秒打印一个数字和时间戳
def main():
    sys.stdout.write('Daemon started with pid %d\n' % os.getpid())
    sys.stdout.write('Daemon stdout output\n')
    sys.stderr.write('Daemon stderr output\n')
    app.run(host='0.0.0.0',port=80)




if __name__ == "__main__":
      daemonize('/dev/null','/tmp/daemon_stdout.log','/tmp/daemon_error.log')
      main()
