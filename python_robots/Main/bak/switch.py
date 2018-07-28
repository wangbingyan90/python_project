card=[]

def fun1():  #往card中添加元素
    name=input(">>>")
    card.append(name)
    return name
 
def fun2():   #遍历card
    for name in card:
        print(name)
 
def fun3():   #退出程序 
    exit(0)


def function(x):
    swicher = {              #定义一个map，相当于定义case：func()
        '1':fun1,
        '2':fun2,
        '3':fun3,
        '4':lambda :print('default function')
    }
    func = swicher.get(x,'4') #从map中取出方法
    return func()   