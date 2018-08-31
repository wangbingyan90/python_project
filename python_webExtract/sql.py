import sqlite3
import time

class Sql:

    def __init__(self):
        self.conn= sqlite3.connect('web2.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists page(name text)')
        self.cursor.execute('create table if not exists identifier(name text)')
        self.cursor.execute('create table if not exists connext(name text, img text,connext text)')

    
    # sql运行添加函数
    def sqlExe(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            f = open('err.txt', 'a+',encoding='utf-8')
            f.write('数据保存失败：'+time.strftime("%Y-%m-%d %H:%M:%S")+sql+"\n")
            f.close()
            return ""


    # sql查找单个函数
    def sqlSelectOne(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()


    # 添加identifier
    def addPage(self,name):
        sql = "insert into page(name)values('%s') " % (name)
        self.sqlExe(sql)


    # 是否存在identifier
    def existpage(self,name):
        sql = "select * from page where name = '%s'" %(name)
        return self.sqlSelectOne(sql) is not None

    # 添加identifier
    def addIdentifier(self,name):
        sql = "insert into identifier(name)values('%s') " % (name)
        self.sqlExe(sql)


    # 是否存在identifier
    def existIdentifier(self,name):
        sql = "select * from identifier where name = '%s'" %(name)
        return self.sqlSelectOne(sql) is not None


    # 添加connext
    def addConnext(self,name,img,connext):
        sql = "insert into connext(name, img, connext)values('%s','%s','%s')" % (name,img,connext)
        self.sqlExe(sql)