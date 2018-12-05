from queue import Queue
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


"""
线程安全的广播
"""


class GroupMessage():
    def __init__(self, profix="", idlist=[], loglevel=logging.ERROR):
        self.profix = profix
        self.idlist = idlist
        self.init = False
        self.log = logging
        self.log.basicConfig(level=loglevel,
                             format=self.__class__.__name__ + " %(asctime)s - %(levelname)s - - %(message)s",
                             datefmt="%Y-%m/%d %H:%M:%S %p")

    def initAllGroup(self):
        try:
            self.allQueue = {}
            self.setGroup = {}
            for id in self.idlist:
                self.allQueue[self.profix + str(id)] = Queue()
            self.init = True
            return True
        except Exception as e:
            self.log.debug(e)
            return False

    def removeQueue(self, id):
        if self.profix + str(id) in self.allQueue.keys():
            del self.allQueue[self.profix + str(id)]
            return True
        return False

    def sendAllQueue(self, message=""):
        try:
            for queue in self.allQueue.keys():
                self.allQueue[queue].put(message)
            return True
        except Exception as e:
            self.log.debug(e)
            return False

    def addAllQueue(self, id):
        self.allQueue[self.profix + str(id)] = Queue()
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
            self.allQueue[self.profix + str(id)] = Queue()
            if group in self.setGroup.keys():
                self.setGroup[group].add(self.profix + str(id))
                return self.setGroup[group]
            else:
                self.setGroup[group] = set()
                self.setGroup[group].add(self.profix + str(id))
                return self.setGroup[group]

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
        for id in self.allQueue.keys():
            del self.allQueue[id]
        self.allQueue.clear()

    def sendGroup(self, group="", message=""):
        if group in self.setGroup.keys():
            self.log.debug(self.setGroup[group])
            for queuename in self.setGroup[group]:
                self.log.debug(queuename)
                if queuename in self.allQueue.keys():
                    self.allQueue[queuename].put(message)
                    self.log.debug(self.allQueue)
            return True
        else:
            return False

    def push(self, id=None, message=""):
        if self.profix + str(id) in self.allQueue.keys():
            try:
                self.allQueue[self.profix + str(id)].put(message)
                return True
            except Exception as e:
                self.log.debug(e)
                return False
        else:
            try:
                self.allQueue[self.profix + str(id)] = Queue()
                self.allQueue[self.profix + str(id)].put(message)
                return True
            except Exception as e:
                self.log.debug(e)
                return False

    def poll(self, id=None):
        if self.profix + str(id) in self.allQueue.keys():
            try:
                return self.allQueue[self.profix + str(id)].get_nowait()
            except Exception as e:
                self.log.debug(e)
                return None
        else:
            return None


"""
可以被序列化的广播
"""


class GroupMessageUnSafe():
    def __init__(self, profix="", idlist=[], loglevel=logging.ERROR):
        self.profix = profix
        self.idlist = idlist
        self.init = False
        self.log = logging
        self.log.basicConfig(level=loglevel,
                             format=self.__class__.__name__ + " %(asctime)s - %(levelname)s - - %(message)s",
                             datefmt="%Y-%m/%d %H:%M:%S %p")

    def initAllGroup(self):
        try:
            self.allQueue = {}
            self.setGroup = {}
            for id in self.idlist:
                self.allQueue[self.profix + str(id)] = deque()
            self.init = True
            return True
        except Exception as e:
            self.log.debug(e)
            return False

    def removeQueue(self, id):
        if self.profix + str(id) in self.allQueue.keys():
            del self.allQueue[self.profix + str(id)]
            return True
        return False

    def sendAllQueue(self, message=""):
        try:
            for queue in self.allQueue.keys():
                self.allQueue[queue].append(message)
            return True
        except Exception as e:
            self.log.debug(e)
            return False

    def addAllQueue(self, id):
        self.allQueue[self.profix + str(id)] = deque()
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
            self.allQueue[self.profix + str(id)] = deque()
            if group in self.setGroup.keys():
                self.setGroup[group].add(self.profix + str(id))
                return self.setGroup[group]
            else:
                self.setGroup[group] = set()
                self.setGroup[group].add(self.profix + str(id))
                return self.setGroup[group]

    def sendGroup(self, group="", message=""):
        if group in self.setGroup.keys():
            self.log.debug(self.setGroup[group])
            for queuename in self.setGroup[group]:
                self.log.debug(queuename)
                if queuename in self.allQueue.keys():
                    self.allQueue[queuename].append(message)
                    self.log.debug(self.allQueue)
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
        for id in self.allQueue.keys():
            del  self.allQueue[id]
        self.allQueue.clear()

    def push(self, id=None, message=""):
        if self.profix + str(id) in self.allQueue.keys():
            try:
                self.allQueue[self.profix + str(id)].append(message)
                return True
            except Exception as e:
                self.log.debug(e)
                return False
        else:
            try:
                self.allQueue[self.profix + str(id)] = deque()
                self.allQueue[self.profix + str(id)].append(message)
                return True
            except Exception as e:
                self.log.debug(e)
                return False

    def poll(self, id=None):
        if self.profix + str(id) in self.allQueue.keys():
            try:
                return self.allQueue[self.profix + str(id)].popleft()
            except Exception as e:
                self.log.debug(e)
                return None
        else:
            return None


"""
带自自动保存的广播
"""


class GroupMessageUnSafeSaveDisk(GroupMessageUnSafe):

    def __init__(self, profix="", idlist=[], loglevel=logging.ERROR,queue =""):
        super().__init__(profix="", idlist=[], loglevel=logging.ERROR)
        self.allQueue = loads(self.db["allQueue"])
        self.queue_name = queue+"_group_message.db"

    def autoSave(self, time=10):
        try:
            LoopTimer(time, self.save).start()
        except Exception as e:
            self.log.debug(e)

    def initAllGroup(self):
        try:
            status = self.load()
            if status:
                return status
            else:
                self.allQueue = {}
                self.setGroup = {}
                for id in self.idlist:
                    self.allQueue[self.profix + str(id)] = deque()
                self.init = True
            return True
        except Exception as e:
            self.log.debug(e)
            return False

    def save(self):
        try:
            self.db = gnu.open(self.queue_name, "c")
            self.db["setGroup"] = dumps(self.setGroup)
            self.db["allQueue"] = dumps(self.allQueue)
            self.db["profix"] = dumps(self.profix)
            self.db.sync()
            self.log.debug("init ok")
            return True
        except Exception as e:
            self.log.debug(e)
            return False
        finally:
            self.db.close()

    def load(self):
        try:
            self.db = gnu.open(self.queue_name, "c")
            self.setGroup = loads(self.db["setGroup"])
            self.profix = loads(self.db["profix"])
            self.idlist = []
            for id in self.allQueue.keys():
                self.idlist.append(id)
            self.log.debug("load ok")
            return True
        except Exception as e:
            self.log.debug(e)
            return False
        finally:
            self.db.close()


"""
基于gnu数据库的队列
"""


class GnuQueue():

    def __init__(self, queue="", loglevel=logging.ERROR):
        self.name = queue
        self.name_write = queue + "__write"
        self.name_read = queue + "__read"
        self.namefile = self.name + "_gunQueue.db"
        self.index = gnu.open(queue + "_index.db", "c")
        self.queue = gnu.open(self.namefile, "c")
        self.write_id = self.index.get(self.name_write, b"1").decode()
        self.read_id = self.index.get(self.name_read, b"1").decode()
        self.log = logging
        self.log.basicConfig(level=loglevel,
                             format=self.__class__.__name__ + " %(asctime)s - %(levelname)s - - %(message)s",
                             datefmt="%Y-%m/%d %H:%M:%S %p")

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
            del self.queue["key_" + self.read_id - 1]
            self.index.sync()
            self.queue.sync()

    def clear(self):
        try:
            self.queue.clear()
            self.index.clear()
        except Exception as e:
            self.log.debug(e)
            return None
        finally:
            self.index.sync()
            self.queue.sync()

    def close(self):
        self.queue.close()
        self.index.close()
