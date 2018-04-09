# coding:utf-8
from hashlib import sha1
from flask import Flask, request
import time

#
#接收 查看数据
#

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
		print data
		return 'msg'
 
if __name__ == '__main__':
  app.run(host='0.0.0.0',port=80)
