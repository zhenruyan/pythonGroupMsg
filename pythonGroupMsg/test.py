# import pythonGroupMsg as lib
import datetime
import logging
from pythonGroupMsg import lib
e = []
if __name__ == '__main__':
    # queue = lib.DQueue()
    # for a in range(1,100):
    #     # print(queue.pull())
    #     print(queue.getSize())
    #     queue.push("a"+str(a))
    #
    # queue.clear()
    # print(queue.getSize())
    aatime = datetime.datetime.now()
    size = 1000
    for c in range(0,size):
        e.append(c)
    print(lib)
    a = lib.GroupMessage(profix="id:", idlist=e)
    a.initAllGroup()

    print(str(size)+" queue init",(datetime.datetime.now() -aatime).microseconds/1000000,"s")
    print(a.pull(id=2))

    bbtime = datetime.datetime.now()
    ssize= 10
    for d in range(1,ssize):
        a.sendAllQueue("hello world"+str(d))
    print(str(ssize)+" message send on queue",(datetime.datetime.now() - bbtime).microseconds/1000000,"s")
    a.addGroup("chat",660)
    a.addGroup("chat",661)
    a.addGroup("chat",662)
    a.sendGroup("chat","helloworldsadasdasd")
    a.sendGroup("chat","helloworldsadasdasdas")
    for _ in range(0,2):
        print(a.pull(660))
        print(a.pull(661))
        print(a.pull(662))
    a.removeIdOfGroup("chat",660)
    a.sendGroup("chat","helloworldsadasdasd")
    a.sendGroup("chat","helloworldsadasdasdas")
    for _ in range(0,2):
        print(a.pull(660))
        print(a.pull(661))
        print(a.pull(662))
    a.removeGroup("chat")
    print(a.setGroup)
    print(a.allQueue)
    a.removeQueue(660)
    a.removeQueue(1)
    a.removeQueue(2)
    print(a.allQueue)
    a.clearQueue()
    a.clearGroup()
    print(a.setGroup)
    print(a.allQueue)


