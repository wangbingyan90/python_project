import requests
import re,time
from lxml import etree
import random
from multiprocessing.pool import Pool
# import sqlite3

from sql import Sql


class Main:

    def __init__(self):
        pass

    
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
            print('数据获取失败:'+url)
            time.sleep(2)
            r = requests.get(url,timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text

    # 查找页面
    def parsePash(self,n):
        sql = Sql()
        for i in range(15):
            url = 'https://www.3sgif.com/gif/page/%d/' % (i+n*15+1)
            html = self.httpRequest(url)
            add = re.findall(r'https://www.3sgif.com/(\d*).html',html[9500:20000])
            for j in range(int(len(add)/2)):
                url = 'https://www.3sgif.com/%s.html' % (add[j*2])
                print(add[j*2])
                self.parseOne(url,sql)
                

    # 分析页面2
    def parseXpath(self,wb_data,sql):
        html = etree.HTML(wb_data)
        html_data = html.xpath('/html/body/section/div/div/article/p')
        name = ''
        con = ''
        for i in html_data:

            if i.text is not None:
                con = con + i.text
                # add = re.search(r'(\w+-? ?\w*\d*)',i.text)
                
                # print(i.text)
                # if add is not None:
                #     name = add[0].upper()
        # <>,/,\,|,""
        con = con[:-9].replace(' ','').replace('\t','').replace('?','').replace('*','').replace(':','').replace('/','').replace('\\','').replace('|','').replace('<','').replace('>','')[:200]
        # print(con)
        name = re.search(r'(\w+-? ?\w+\d+)',con,re.A)
        if name is not None:
            print(name[0])
        else:
            print('为空：'+con)
        html_data = html.xpath('/html/body/section/div/div/article/p/a/img/@src')
        for j in html_data:
            self.savejpg(j,str(random.randint(0,10000)) + con + '.jpg')
        

    # 分析页面
    def parseOne(self,url,sql):
        html = self.httpRequest(url)
        add = re.findall(r'<span>(\d*)</span></a></div>',html[11000:14000])
        max = int(add[0])
        i = 1
        # print(max)

        print(url)
        if not sql.existpage(url):
            sql.addPage(url)
            self.parseXpath(html,sql)

        while max > i:
            i = i + 1
            url2 = url + '/' + str(i) + '/'
            print(url2)
            
            if not sql.existpage(url2):
                html = self.httpRequest(url2)
                sql.addPage(url)
                self.parseXpath(html,sql)


    # 保存图片
    def savejpg(self,url,name):
        r = requests.get(url)
        with open('E:/date/' + name, 'wb') as f:
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
    # t.run()

    # t.parseOne('https://www.3sgif.com/38211.html')
    # t.parsePash(0)
    # t.run()
    # t.parsePash(0)
    
    wb_data = t.httpRequest('https://www.3sgif.com/37055.html/22/')
    sql = Sql()
    t.parseXpath(wb_data,sql)