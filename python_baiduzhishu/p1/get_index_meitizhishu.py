from config import COOKIES
import config
from urllib.parse import urlencode
from collections import defaultdict
import datetime
import requests
import json
import os

# wby 2019-1

headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}


class BaiduIndex:
    """
        百度媒体指数
    """

    # para = {'关键字':'万科',            # 不可省略，多个关键词使用分割
    #     '地区':'广州，北京',              # 不可省略，默认为全部配置地区检索
    #     '平台':'',              # 可省略，默认为pc+移动，1：pc; 2: 移动； 3：pc+移动
    #     '开始日期':'',          # 可省略，默认为最早的时间 如2018-1-1
    #     '结束日期':'',          # 可省略，默认为昨天
    #     }
    def __init__(self, para):

        self.nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        self.data = []
        keyword = para['关键字']
        self.keywords = keyword if isinstance(keyword, list) else keyword.split('，')
        area = para['地区']
        self.areas = area if isinstance(area, list) else area.split('，')
        self._all_kind = ['all', 'pc', 'wise']
        self.setKind(para['平台'])

        for keyword in self.keywords:
            self.result = None
            self.result = {area: defaultdict(list) for area in self.areas}
            self.setDay(para['开始日期'],para['结束日期'],keyword)
            for area in self.areas:
                self.get_result(self.start_date,self.end_date,area,keyword)
            print(keyword + '查询完成')
            self.print_data(keyword)


    def setKind(self,kind):
        if kind == 1:
            self.kind = 'pc'
        elif kind == 2:
            self.kind = 'wise'
        else:
            self.kind = 'all'


    # 设置时间
    def setDay(self,start_date,end_date,keyword):
        
        if start_date == '':
            encrypt_datas = self.get_encrypt_datas_all(keyword)
            self.start_date = encrypt_datas['startDate']
        else:
            self.start_date = start_date
        if end_date == '':
            self.end_date = str(datetime.datetime.now()-datetime.timedelta(days=1))[:10]
        else:
            self.end_date == end_date



    def get_result(self,start_date, end_date,area,keyword):
        '''
        获取结果
        '''
        self.time_range_list = self.get_time_range_list(start_date, end_date)
        for start_date, end_date in self.time_range_list:
            encrypt_data, uniqid = self.get_encrypt_datas(start_date, end_date,area,keyword)
            key = self.get_key(uniqid)
            c = self.decrypt_func(key, encrypt_data['data'])
            self.data = self.data + c
        self.result[area][self.kind].append(self.data)
        self.data=[]
        


    def get_encrypt_datas_all(self,keyword):
        
        request_args = {
            'word': keyword,
            'area': 0,
        }
        url = 'http://index.baidu.com/api/SearchApi/index?' + urlencode(request_args)
        datas = json.loads(self.http_get(url))
        encrypt_datas = datas['data']['userIndexes'][0]['all']
        return encrypt_datas
    

    def get_encrypt_datas(self, start_date, end_date,area,keyword):
        """
        :start_date; str, 2018-10-01
        :end_date; str, 2018-10-01
        """
        request_args = {
            'area': int(config.area[area]),
            'word': keyword,
            'startDate': str(start_date)[:10],
            'endDate': str(end_date)[:10],
        }
        url = 'http://index.baidu.com/api/NewsApi/getNewsIndex?' + urlencode(request_args)
        html = self.http_get(url)
        datas = json.loads(html)
        uniqid = datas['data']['uniqid']
        encrypt_datas = []
        for single_data in datas['data']['index']:
            encrypt_datas.append(single_data)
        return (encrypt_datas[0], uniqid)

    def get_key(self, uniqid):
        """
        """
        url = 'http://index.baidu.com/Interface/api/ptbk?uniqid=%s' % uniqid
        html = self.http_get(url)
        datas = json.loads(html)
        key = datas['data']
        return key

    def print_data(self,keyword):
        """
        """
        file = open(str(self.nowTime) + '媒体指数.csv','a')
        file.write('时间,')

        time_len = len(self.result[self.areas[0]]['all'][0])
        start_date = self.start_date
        cur_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        for i in range(time_len):
            file.write(cur_date.strftime('%Y-%m-%d'))
            cur_date += datetime.timedelta(days=1)
            file.write(',')
        file.write('\n')
        
        for area in self.areas:
            file.write(keyword)
            for i in range(time_len):
                file.write(','+self.result[area]['all'][0][i])
        file.write('\n')
        file.close()


    @staticmethod
    def http_get(url, cookies=COOKIES):
        headers['Cookie'] = cookies
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None

    @staticmethod
    def get_time_range_list(startdate, enddate):
        """
        max 6 months
        """
        date_range_list = []
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            tempdate = startdate + datetime.timedelta(days=180)
            if tempdate > enddate:
                date_range_list.append((startdate, enddate))
                return date_range_list
            date_range_list.append((startdate, tempdate))
            startdate = tempdate + datetime.timedelta(days=1)

    @staticmethod
    def decrypt_func(key, data):
        """
        decrypt data
        """
        a = key
        i = data
        n = {}
        s = []
        for o in range(len(a)//2):
            n[a[o]] = a[len(a)//2 + o]
        for r in range(len(data)):
            s.append(n[i[r]])
        return ''.join(s).split(',')

if __name__ == '__main__':
    para = {'关键字':'万科，万达',            # 不可省略，多个关键词使用分割
            '地区':'全国',              # 可省略，默认为全部配置地区检索，媒体指数词条不写
            '平台':'',              # 可省略，默认为pc+移动，1：pc; 2: 移动； 3：pc+移动
            '开始日期':'',          # 可省略，默认为最早的时间 如2018-1-1
            '结束日期':'',          # 可省略，默认为今天
            }
    baidu_index = BaiduIndex(para)
