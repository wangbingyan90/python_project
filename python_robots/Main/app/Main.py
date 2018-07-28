from Login import WeChatLogin
import time
import Static,Log

if __name__ == '__main__':
    login = WeChatLogin()
    login.doLogin()
    while True:
        login.sendMsg()
        time.sleep(10)