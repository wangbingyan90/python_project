import sqlite3
import time

#
# wby 2018
# python 自带sqlLit服务 无需安装
class SqlLitUtil:

    def __init__(self):
        self.conn= sqlite3.connect('wx.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists message (time integer, message text, nickname text, fromto text)')
        self.cursor.execute('create table if not exists friendToid (name text, id text)')



    def __del__(self):
        super()
        self.conn.close()


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


    # sql查找全部函数
    def sqlSelectAll(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    

    # sql查找单个函数
    def sqlSelectOne(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()


    # 添加联系人
    def addContracts(self,data):
        self.sqlExe("delete from friendToid")
        for contract in data:
            # print(contract['RemarkName'])
            # print(contract['NickName'])
            # print(contract['UserName'])
            sql = "insert into friendToid(name,id)values('%s','%s') " % (contract['NickName'],contract['UserName'])
            self.sqlExe(sql)


    def selectIdbyName(self,name):
        sql = "select * from friendToid where name = '%s'" %(name)
        return self.sqlSelectOne(sql)[1]


    def selectNamebyId(self,id):
        sql = "select * from friendToid where id = '%s'" %(id)
        return self.sqlSelectOne(sql)[0]


if __name__  == "__main__":
    sql = SqlLitUtil()
    print(sql.selectIdbyName('小不点'))
