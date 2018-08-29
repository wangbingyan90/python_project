import requests
import re
from lxml import etree
from multiprocessing.pool import Pool
# import sqlite3


class Main:

    def __init__(self):
        pass
        # conn= sqlite3.connect('web.db')
        # cursor = conn.cursor()
        # cursor.execute('create table if not exists parse (parse integer)')
        # cursor.execute('create table if not exists friendToid (jpg text, con text)')

    
    # 网络请求
    def httpRequest(self, url):
        try:
            r = requests.get(url,timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            # print(r.status_code)
            # print(r.text)
            return r.text
        except:
            print('数据获取失败')
            return ""

    # 查找页面
    def parsePash(self,n):
        # conn= sqlite3.connect('web.db')
        # cursor = conn.cursor()
        for i in range(15):
            url = 'https://www.3sgif.com/gif/page/%d/' % (i+n*15+1)
            html = self.httpRequest(url)
            add = re.findall(r'https://www.3sgif.com/(\d*).html',html[9500:20000])
            for j in range(int(len(add)/2)):
                url = 'https://www.3sgif.com/%s.html' % (add[j*2])
                self.parseOne(url)
                


    # 分析页面
    def parseOne(self,url):
        html = self.httpRequest(url)
        add = re.findall(r'src=\"(.*?.jpg).*?<p>(.*?)</p>.*?<span>(\d*)</span></a></div>',html[10000:14000],re.S)
        max = int(add[0][2])
        print(url)
        print(add[0][0])
        print(add[0][1])
        self.savejpg(add[0][0],add[0][1]+'.jpg')
        i = 1
        while max > i:
            i = i + 1
            url2 = url + '/' + str(i) + '/'
            html = self.httpRequest(url2)
            add = re.findall(r'src=\"(.*?.jpg).*?<p>(.*?)</p>',html[10000:13000],re.S)
            name = re.search(r'(\w*-\d*)',add[0][1])
            print(url2)
            print(add[0][0])
            print(add[0][1])
            print(name)
            self.savejpg(add[0][0],add[0][1]+'.jpg')



    # 保存图片
    def savejpg(self,url,name):
        r = requests.get(url)
        with open('E:/data/' + name, 'wb') as f:
            f.write(r.content)
        f.close()

    # 运行
    def run(self):
        print("开始")
        groups = ([x for x in range(4)])
        pool = Pool()
        pool.map(self.parsePash, groups)
        pool.close()
        pool.join()



if __name__ == '__main__':
    t = Main()
    # t.parsePash(0)
    # t.run()
    # t.parsePash(0)
    # t.parseOne('https://www.3sgif.com/37990.html/6/')
    wb_data = t.httpRequest('https://www.3sgif.com/37990.html/6/')
    html = etree.HTML(wb_data)
    html_data = html.xpath('/html/body/section/div/div/article/p')
    print(1)
    # print(html_data[0].text)
    for i in html_data:
        print(i.text)
        if i.text is not None:
            add = re.search(r'(\w*-\d*)',i.text)
            if add is not None:
                print(add[0])
    # /html/body/section/div/div/article/p[2]
    html_data = html.xpath('/html/body/section/div/div/article/p/a/img/@src')
    print(html_data)