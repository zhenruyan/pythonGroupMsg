import os
from abc import ABCMeta,abstractmethod
from collections import deque
try:
    from dbm import gnu
except Exception as e:
    try:
        import dbm as gnu
    except Exception as e:
        from dbm import dumb as gnu
from pickle import dumps, loads
from threading import Timer
import logging
from queue import Queue

##循环loop定时器
class LoopTimer(Timer):
    def __init__(self, interval, function, *args, **kwargs):
        Timer.__init__(self, interval, function, args, kwargs)

    def run(self):
        while True:
            self.finished.wait(self.interval)
            if self.finished.is_set():
                self.finished.set()
                break
            self.function(*self.args, **self.kwargs)


# 定时执行注解
def delayed(seconds):
    def decorator(f):
        def wrapper(*args, **kargs):
            t = LoopTimer(seconds, f, args, kargs)
            t.start()

        return wrapper

    return decorator


# 单次定时器
class OneTimer(Timer):
    def __init__(self, interval, function, *args, **kwargs):
        Timer.__init__(self, interval, function, args, kwargs)


class QueueInstantiate(metaclass=ABCMeta):
    def __init__(self,name="",dir=None):
        pass
    @abstractmethod
    def push(self,message):
        pass
    @abstractmethod
    def pull(self):
        pass
    @abstractmethod
    def clear(self):
        pass
    @abstractmethod
    def close(self):
        pass
    @abstractmethod
    def getSize(self):
        pass


"""
基于gnu数据库的队列
"""
class GnuQueue(QueueInstantiate):

    def __init__(self, name="",dir=None, loglevel=logging.ERROR):
        self.name = name
        self.name_write = name + "__write"
        self.name_read = name + "__read"
        self.namefile = self.name + "_gunQueue.db"
        self.log = logging
        self.log.basicConfig(level=loglevel,
                             format=self.__class__.__name__ + " %(asctime)s - %(levelname)s - - %(message)s",
                             datefmt="%Y-%m/%d %H:%M:%S %p")
        if not dir == None:
            self.dir =  dir
            if not os.path.exists(self.dir):
                os.mkdir(self.dir)
            self.index = gnu.open(self.dir + "/" + name + "_index.db", "c")
            self.queue = gnu.open(self.dir + "/" + self.namefile, "c")
        else:
            os.mkdir("queue_data")
            self.index = gnu.open("queue_data" + "/" + name + "_index.db", "c")
            self.queue = gnu.open("queue_data" + "/" + self.namefile, "c")

        self.write_id = self.index.get(self.name_write, b"1").decode()
        self.read_id = self.index.get(self.name_read, b"1").decode()

    def push(self, message=""):
        try:
            self.queue["key_" + self.write_id] = str(message)
            return True
        except Exception as e:
            self.log.debug(e)
            return False
        finally:
            self.write_id = str(int(self.write_id) + 1)
            self.index[self.name_write] = str(self.write_id)
            self.index.sync()
            self.queue.sync()

    def pull(self):
        try:
            val = self.queue.get("key_" + self.read_id, None)
            if not val == None:
                self.read_id = str(int(self.read_id) + 1)
                self.index[str(self.name_read)] = str(self.read_id)
            return val
        except Exception as e:
            self.log.debug(e)
            return None
        finally:
            if int(self.read_id)>1:
                del self.queue["key_" + str(int(self.read_id) - 1)]
            else:
                self.clear()
            self.index.sync()
            self.queue.sync()

    def clear(self):
        try:
            for key in list(self.queue.keys()):
                del self.queue[key]
            for key in list(self.index.keys()):
                del self.index[key]

        except Exception as e:
            self.log.debug(e)
            return None
        finally:
            self.index.sync()
            self.queue.sync()

    def close(self):
        self.queue.close()
        self.index.close()

    def getSize(self):
        return len(list(self.queue.keys()))
"""
lockQueue
"""
class LockQueue(QueueInstantiate):
    def __init__(self,name=None,dir=None):
        self.queue = Queue()
    def push(self,message):
        self.queue.put(message)
    def pull(self):
        try:
            return self.queue.get_nowait()
        except Exception as e:
            return None

    def clear(self):
        self.queue = Queue()

    def getSize(self):
        return self.queue.qsize()
    def close(self):
        pass
"""
可以被序列化的queue
"""
class DQueue(QueueInstantiate):
    def __init__(self,name=None,dir=None):
       self.queue = deque()
    def push(self,message):
        self.queue.append(message)
    def pull(self):
        try:
            return self.queue.popleft()
        except Exception as e:
            return None
    def getSize(self):
        return len(self.queue)
    def clear(self):
        self.queue.clear()
    def close(self):
        pass

"""
队列广播
"""
class GroupMessage():
    def __init__(self,name="GroupMessage",profix="", idlist=[],queue = DQueue):
        self.profix = profix
        self.idlist = idlist
        self.init = False
        self.allQueue = {}
        self.setGroup = {}
        self.queue = queue
        self.name = name

    def initAllGroup(self):
        try:
            for id in self.idlist:
                self.allQueue[self.profix + str(id)] = self.queue(name=str(id),dir=self.name)
            self.init = True
            return True
        except Exception as e:
            return False

    def removeQueue(self, id):
        if self.profix + str(id) in self.allQueue.keys():
            self.allQueue[self.profix + str(id)].close()
            del self.allQueue[self.profix + str(id)]
            return True
        return False

    def sendAllQueue(self, message=""):
        try:
            for queue in self.allQueue.keys():
                self.allQueue[queue].push(message)
            return True
        except Exception as e:
            return False

    def addAllQueue(self, id):
        self.allQueue[self.profix + str(id)] = self.queue(name=str(id),dir=self.name)
        self.idlist.append(id)

    def addGroup(self, group="", id=None):
        if (self.profix + str(id)) in self.allQueue.keys():
            if group in self.setGroup.keys():
                self.setGroup[group].add(self.profix + str(id))
                return self.setGroup[group]
            else:
                self.setGroup[group] = set()
                self.setGroup[group].add(self.profix + str(id))
                return self.setGroup[group]
        else:
            self.allQueue[self.profix + str(id)] = self.queue(name=str(id),dir=self.name)
            if group in self.setGroup.keys():
                self.setGroup[group].add(self.profix + str(id))
                return self.setGroup[group]
            else:
                self.setGroup[group] = set()
                self.setGroup[group].add(self.profix + str(id))
                return self.setGroup[group]

    def sendGroup(self, group="", message=""):
        if group in self.setGroup.keys():
            for queuename in self.setGroup[group]:
                if queuename in self.allQueue.keys():
                    self.allQueue[queuename].push(message)
            return True
        else:
            return False

    def removeIdOfGroup(self, group, id):
        if group in self.setGroup.keys():
            if (self.profix + str(id)) in self.setGroup[group]:
                self.setGroup[group].remove((self.profix + str(id)))
                return True
            return False
        return False

    def removeGroup(self, group):
        if group in self.setGroup.keys():
            del self.setGroup[group]
            return True
        return False

    def clearGroup(self):
        self.setGroup.clear()

    def clearQueue(self):
        for id in list(self.allQueue.keys()):
            self.allQueue[id].close()
            del  self.allQueue[id]
        self.allQueue.clear()

    def push(self, id=None, message=""):
        if self.profix + str(id) in self.allQueue.keys():
            try:
                self.allQueue[self.profix + str(id)].push(message)
                return True
            except Exception as e:
                return False
        else:
            try:
                self.allQueue[self.profix + str(id)] = self.queue(name=str(id),dir=self.name)
                self.allQueue[self.profix + str(id)].push(message)
                return True
            except Exception as e:
                return False

    def pull(self, id=None):
        if self.profix + str(id) in self.allQueue.keys():
            try:
                return self.allQueue[self.profix + str(id)].pull()
            except Exception as e:
                return None
        else:
            return None


