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



    def __del__(self):
        super()
        self.conn.close()
        self.cursor.close()


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


    # 查找歌单id
    def selecthotPlaylist(self):
        sql = 'select id from hotPlaylist'
        return self.sqlSelectAll(sql)

    def selectfinshPlaylist(self,id):
        sql = 'select id from hotPlaylistnew where id = %d' % (id) 
        return self.sqlSelectOne(sql) is None

    # 查找最小id歌手
    def selectSinger(self,singersname):
        sql = "select Singer_Id from Singer where Singer_name= '%s'" % (singersname.replace("'", "\\'"))
        # print(sql)
        singerid = self.sqlSelectOne(sql)
        if singerid is None:
            sql = 'select min(Singer_Id) from Singer'
            return self.sqlSelectOne(sql)[0]-1
        return singerid[0]


    # 添加标签
    def addTag(self,tagname):
        sql = "select Tags_Id from Tags where Tags_name= '%s'" % (tagname)
        tageId = self.sqlSelectOne(sql)
        if tageId is None:
            sqladd = "insert into Tags(Tags_name)values('%s') " % (tagname)
            self.sqlExe(sqladd)
            tageId = self.sqlSelectOne(sql)[0]
            return tageId
        return tageId[0]


    # 添加标签组
    def addTags(self,tags,List_Id):
        for tagname in tags:
            tageId = self.addTag(tagname)
            sql = "insert into Relationsippt(List_Id,Tags_Id)values(%d,%d) " % (List_Id,tageId)
            # print(sql)
            self.sqlExe(sql)

        
    # 添加详细歌单
    def addPlayList(self,data):
        sql = "insert into PlayList(List_Id,List_Name,Author_Id,List_img,\
         PlayCount,List_creatTime,List_updataTime,Description,SubscribedCount,\
        ShareCount,CommentCount)values(%d,'%s',%d,'%s',%d,%d,%d,'%s',%d,\
        %d,%d)" % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],\
        data[7],data[8],data[9],data[10])
        # print(sql)
        self.sqlExe(sql)


    # 添加歌单id
    def addhotPlaylist(self,List_Id):
        sql = "insert into hotPlaylist(id)values(%d) " % (List_Id)
        # print(sql)
        self.sqlExe(sql)

    # 添加歌单id
    def addfinshPlaylist(self,List_Id):
        sql = "insert into hotPlaylistnew(id)values(%d) " % (List_Id)
        # print(sql)
        self.sqlExe(sql)


    # 添加作者
    def addAuthor(self,data):
        sql = "insert into Author(Author_Id,Author_Name,Signature,city,Author_img)values(%d,'%s','%s',%d,'%s') " % (data[0],data[1],data[2],data[3],data[4])
        # print(sql)
        self.sqlExe(sql)

    
    # # 添加歌单与作者连接
    # def addRelationsip(self,data):
    #     sql = "insert into Relationsip(List_Id,Music_Id)values(%d,%d) " % (data[0],data[1])
    #     print(sql)
    #     self.sqlExe(sql)

    
    # 添加歌曲
    def addMusic(self,data):
        sql = "insert into Music(Music_Id,Music_Name,Music_img,\
        Music_creatTime,Popularity,Description,Duration,Company,SubType)\
        values(%d,'%s','%s',%d,%d,'%s',%d,'%s','%s') " % (data[0],data[1],\
        data[2],data[3],data[4],data[5],data[6],data[7],data[8])
        # print(sql)
        self.sqlExe(sql)

    
    # 添加歌手
    def addSinger (self,data):
        sql = "insert into Singer(Singer_Id,Singer_name)values(%d,'%s') " % (data[0],data[1].replace("'", "\\'"))
        # print(sql)
        self.sqlExe(sql)

    
    # 添加评论
    def addComment(self,data):
        sql = "insert into Comment(Comment_Id,Comment_content,LikedCount,Music_Id,Author_Id,\
        Comment_creatTime)values(%d,'%s',%d,%d,%d,%d) " % (data[0],data[1],data[2],data[3],data[4],data[5])
        # print(sql)
        self.sqlExe(sql)


    # 添加关系
    def addRelationsip(self,data):
        sql = "insert into %s(%s,%s)values(%s,%s) " % (data[0],data[1],data[2],data[3],data[4])
        # print(sql)
        self.sqlExe(sql)


if __name__  == "__main__":
    sql = SqlLitUtil()