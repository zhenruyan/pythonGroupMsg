import clib
import datetime
e = []
if __name__ == '__main__':
    aatime = datetime.datetime.now()
    for c in range(1,99999):
        e.append(c)
    a = clib.GroupMessageUnSafe(profix="id:", idlist=e)
    a.initAllGroup()
    print("99999个队列初始化",(datetime.datetime.now() -aatime).microseconds/1000000,"s")
    bbtime = datetime.datetime.now()
    for d in range(1,100):
        a.sendAllQueue("hello world")
    print("100次发送",(datetime.datetime.now() - bbtime).microseconds/1000000,"s")

    print(a.poll(2))