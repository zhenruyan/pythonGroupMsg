pythonGroupMsg Queue multicast broadcast
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

cython  Broadcasting to multiple queues
========================================

 Recently, I'm going to do something like chat software. After a lot of testing, I've done this thing.

    Performance is 13 times faster than py direct circular transmission


install ::

    pip install pythonGroupMsg




push msg
++++++++

python ::

    import pythonGroupMsg
    import datetime
    import logging
    e = []
    if __name__ == '__main__':
        aatime = datetime.datetime.now()
        for c in range(1,3):
            e.append(c)
        a = pythonGroupMsg.GroupMessage(profix="id:", idlist=e,loglevel=logging.INFO)
        a.initAllGroup()
        print("100000 queue init",(datetime.datetime.now() -aatime).microseconds/1000000,"s")
        bbtime = datetime.datetime.now()
        for d in range(1,10):
            a.sendAllQueue("hello world"+str(d))
        print("100 message send on queue",(datetime.datetime.now() - bbtime).microseconds/1000000,"s")
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











