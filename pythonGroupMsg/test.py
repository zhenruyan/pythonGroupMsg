import pythonGroupMsg as lib
import datetime
import logging
e = []
if __name__ == '__main__':
    aatime = datetime.datetime.now()
    size = 100
    for c in range(0,size):
        e.append(c)
    a = lib.GroupMessage(profix="id:", idlist=e,loglevel=logging.INFO)
    a.initAllGroup()
    print(str(size)+" queue init",(datetime.datetime.now() -aatime).microseconds/1000000,"s")
    bbtime = datetime.datetime.now()
    ssize= 10
    for d in range(1,ssize):
        a.sendAllQueue("hello world"+str(d))
    print(str(ssize)+" message send on queue",(datetime.datetime.now() - bbtime).microseconds/1000000,"s")
    a.addGroup("chat",660)
    a.addGroup("chat",661)
    a.addGroup("chat",662)
    print(a.setGroup)
    a.sendGroup("chat","helloworldsadasdasd")
    a.sendGroup("chat","helloworldsadasdasdas")
    for _ in range(0,2):
        print(a.poll(660))
        print(a.poll(661))
        print(a.poll(662))
    a.removeIdOfGroup("chat",660)
    a.sendGroup("chat","helloworldsadasdasd")
    a.sendGroup("chat","helloworldsadasdasdas")
    for _ in range(0,2):
        print(a.poll(660))
        print(a.poll(661))
        print(a.poll(662))
    a.removeGroup("chat")
    print(a.setGroup)
    print(a.allQueue)
    a.removeQueue(660)
    a.removeQueue(1)
    a.removeQueue(2)
    print(a.allQueue)


