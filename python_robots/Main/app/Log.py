import time

def log(state,context):
    f = open('log.txt', 'a+',encoding='utf-8')
    f.write(state + time.strftime("%Y-%m-%d %H:%M:%S")+'\t' + context+'\n')