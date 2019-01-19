from get_index import BaiduIndex

if __name__ == "__main__":
    para = {'关键字':'万科',            # 不可省略，多个关键词使用分割
            '地区':'广州，北京',              # 可省略，默认为全部配置地区检索
            '平台':'',              # 可省略，默认为pc+移动，1：pc; 2: 移动； 3：pc+移动
            '开始日期':'',          # 可省略，默认为最早的时间 如2018-1-1
            '结束日期':'',          # 可省略，默认为今天
            }
    baidu_index = BaiduIndex(para)
