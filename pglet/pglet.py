# -*- coding: utf-8 -*-

"""multi process and multi greenlet spawn"""

from gevent.queue import Queue
from functools import partial
import gevent
import gipc
import random
import time
import logging

import sys; sys.modules.pop("threading", None)
from gevent import monkey; monkey.patch_all()
from .dictqueue import DictQueue

logger = logging.getLogger("pglet")
logger = logging

def id_generator():
    i = 0
    wall = 1 << 31
    while True:
        i += 1
        if i > wall:
            i = 1
        yield i
        

class Delay(object):
    """future对象: PPool的spawn返回的future对象"""
    
    def __init__(self, ppool, task_id):
        self.ppool = ppool
        self.task_id = task_id
        
    def get(self, block=True, timeout=None):
        """在这里,block不能为False"""
        return self.ppool.results.get(self.task_id, block, timeout)
    
    
class PPool(object):
    """process pool + gevent spawn
    : 1.必须放在入口文件的最开始处调用PPool实例的init函数, 因为子进程会复制主进程空间(包括已有协程)
    : 2.如果需要子进程也包含某些模块/全局变量,可以在模块/全局变量导入后再调用init函数,原则是不能复制过多主进程空间
    Example:
    from share import ppool; ppool.init()
    import sys; sys.modules.pop("threading", None)
    from gevent import monkey; monkey.patch_all()
    import gevent
    
    def foo(a):
        print a
        
    ppool.spawn_sub(foo, "abc")
    
    gevent.wait()
    """
    
    def __init__(self, process_size=1):
        """
        @param process_size: the process pool size
        """
        self.id_generator = id_generator()
        self.process_size = process_size
        self.parent_pipe_ends = []         # 存放process_size个双向pipe的父进程端
        self.child_pipe_ends = []          # 存放process_size个双向pipe的子进程端
        self.processes = []                # 存放process_size个子进程
        self.results = DictQueue()         # 在阻塞模式下存放结果, {task_id:DictQueue()}
        self.loop_get_result_glets = []    # 存放 loop_get_result 产生的process_size个greenlet
        
    def init(self):
        for _ in xrange(self.process_size):
            child_pipe_end, parent_pipe_end =  gipc.pipe(duplex=True)
            self.child_pipe_ends.append(child_pipe_end)
            self.parent_pipe_ends.append(parent_pipe_end)
            p = gipc.start_process(target=self.process_target, args=(child_pipe_end, ), daemon=True)
            self.processes.append(p)
            #p.join()
            
            self.loop_get_result()
            
    def loop_get_result(self):
        """循环读取子进程返回结果"""
        self.n = 0 # 用于测试性能,发布时删除
        def loop(p):
            while 1:
                try:
                    k, v = p.get()
                    if k == -9: # 用于测试性能,发布时删除, =-9时表示该子进程joinall结束
                        self.n += 1
                        if self.n == self.process_size:
                            print "join all completed!!!", time.time()
                        continue
                    self.results.put(k, v, override=True, timeout=None)
                except Exception as e:
                    logger.warning(str(e))
                    break
                
        for p in self.parent_pipe_ends:
            g = gevent.spawn(loop, p)
            self.loop_get_result_glets.append(g)
        
    def process_target(self, child_pipe_end):
        """子进程空间"""
        def callback(g, task_id):
            child_pipe_end.put([task_id, g.value])
        
        taskqs = [] # 用于测试,发布时删除
            
        def loop(child_pipe_end, taskqs):
            while 1:
                try:
                    f, args, kwargs, task_id = child_pipe_end.get()
                    if task_id >= 0:
                        g = gevent.spawn(f, *args, **kwargs)
                        cb = partial(callback, task_id=task_id)
                        g.link(cb)
                    elif task_id == -1: # 用于测试性能,发布时删除, =-1时表示joinall开始
                        taskqs.append([f, args])
                    elif task_id == -2: # 用于测试性能,发布时删除, =-2时表示joinall结束
                        gevent.joinall([gevent.spawn(f, args) for f, args in taskqs])
                        child_pipe_end.put([-9, None])
                    else:
                        gevent.spawn(f, *args, **kwargs)
                except Exception as e:
                    logger.warning(str(e))
                    break
                    
        loop(child_pipe_end, taskqs)
        
    def _benchmark_join_start(self, f, ts=[]):
        parent_pipe_end = self.select_pipe_writer()
        [parent_pipe_end.put([f, args, None, -1]) for args in ts]
    
    def _benchmark_join_end(self):
        for p in self.parent_pipe_ends:
            p.put([None, None, None, -2])

    def select_pipe_writer(self,  sn=None):
        if sn is not None:
            return self.parent_pipe_ends[sn]
        return random.choice(self.parent_pipe_ends)
        
    def _spawn(self, f, args=tuple(), kwargs={}, future=False, timeout=None, sn=None):
        """和gevent.spawn的区别是,如果block=False 就不返回任何值(gevent.spawn返回greenlet),如果block=True,返回f的结果值,而不是greenlet
        @param f: func
        @param args, kwargs: f的参数, ***必须能够pickle序列化***
        @param: future: 是否返回future对象(future.get阻塞获取结果)
        """
        parent_pipe_end = self.select_pipe_writer(sn)
        if future:
            task_id = self.id_generator.next()
            parent_pipe_end.put([f, args, kwargs, task_id])
            delay = Delay(self, task_id)
            return delay
        else:
            parent_pipe_end.put([f, args, kwargs, None])
        
    def spawn(self, f, *args, **kwargs):
        """f的参数和返回值***必须能够pickle序列化***
        @return: 返回future对象,future.get()来阻塞获取结果
        """
        return self._spawn(f, args, kwargs, True, None)
        
    def spawn_sub(self, f, *args, **kwargs):
        """f的参数***必须能够pickle序列化***
        @return: 无 (即:是过程sub)
        """
        return self._spawn(f, args, kwargs, False, None)
        
    def close(self):
        """不再使用时,必须手动调用"""
        try:
            [p.terminate() for p in self.processes]          # 结束子进程
            [g.kill() for g in self.loop_get_result_glets]   # 结束取结果的协程
            [p.close() for p in self.parent_pipe_ends]       # 管道一端关闭即可
        except Exception as e:
            logger.warning(str(e))
        
    def __del__(self):
        self.close()
        
        
        
if __name__ == "__main__":
    def x(a):
        return a
        
    try:
        ppool = PPool(2)
        ppool.init()
        print ppool.spawn(x, "abc").get()
        print ppool.spawn_sub(x, "def")
        ppool.close()
        gevent.wait()
    except KeyboardInterrupt:
        ppool.close()
    

        