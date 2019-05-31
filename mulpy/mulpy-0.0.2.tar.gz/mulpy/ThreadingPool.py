# !/usr/bin/env python
# -*- coding:UTF-8 -*-

import time
import queue
import threading


# 线程池类,经历一万次调用测试,运行过程稳定
class ThreadingPool(object):
    """
    该类会创建一个维护进程,因此当max_threading=10时,实际上会同时运行11个进程
    """
    def __init__(self, max_threading=10):
        # 用于判断当前线程是否关闭,若为True,则线程已经关闭
        self._closed = False
        # 线程队列,队列中的线程时未执行的线程
        self.threading_queue = queue.Queue()
        self.max_threading = max_threading
        # 正在运行的线程池
        self._alive_threads = []
        # 运行结束的线程池
        self._death_threads = []
        self._lock = threading.Lock()
        self._alive_lock = threading.Lock()
        self._joined = False
        self.start_evt = threading.Event()
        self._check_thread = threading.Thread(target=self._check, name='_check')
        self._check_thread.start()
        pass
    
    # 该方法对应一个维护进程,该方法会陷入一个死循环,直至_close为True时停止.
    def _check(self):
        # 等待线程同步
        self.start_evt.wait()
        # 当线程池未关闭
        while self._alive_number() != 0 or self.threading_queue.qsize() != 0:
            # 对后续操作上线程锁
            self._lock.acquire()
            try:
                # 若运行线程数目小于最大线程数目
                if self._alive_number() < self.max_threading:
                    # 判断是否有多的线程任务在队列中
                    if self.threading_queue.qsize() > 0:
                        # 使用get_nowait方法,立即获取一个线程数据
                        t = self.threading_queue.get_nowait()
                        # 将t推送到运行线程缓存中
                        self._alive_threads.append(t)
                        # 启动线程t
                        t.start()
                        # if self._joined:
                        #    t.join()
                else:
                    # 线程数目大于最大运行数目,线程暂停0.01秒
                    time.sleep(0.01)
            finally:
                # 释放线程锁
                self._lock.release()
        return

    # 获取存活线程数目,该方法线程不安全,因此需要在线程安全时调用
    def _alive_number(self):
        self._alive_lock.acquire()
        try:
            self._update_alive()
        finally:
            self._alive_lock.release()
        return len(self._alive_threads)

    # 更新存活线程,该方法线程不安全,因此需要在线程安全时调用
    def _update_alive(self):
        for t in self._alive_threads:
            if not t.is_alive():
                self._alive_threads.remove(t)
                self._death_threads.append(t)
        return

    # 向进程池中添加一个进程,添加后会自动运行
    # 该方法只负责创建线程,并不负责启动线程
    def append(self, target, args, name=None):
        # 创建线程对象
        t = threading.Thread(target=target, args=args, name=name)
        # 使用put_nowait方法,将线程立即放入线程池
        self.threading_queue.put_nowait(t)
        # 同步_check线程
        self.start_evt.set()
        return True
    
    # 关闭线程池入口
    def close(self):
        # 将_closed标志位设置为True
        self._closed = True
        return
    
    # 阻塞主线程,在主线程中调用一个死循环,只有当所有线程结束后才会释放
    def join(self):
        # 判断是否调用过close方法,若未调用过,则会报错
        if self._closed is False:
            # TODO
            # 未来需要自定义异常类
            raise Exception("在调用join方法前必须先调用close方法.")
        if self._joined:
            raise Exception("已经调用过join方法,该方法仅能调用一次")
        # 将joined标志位设置为True
        self._joined = True
        #
        while not (self._alive_number() == 0 and self.threading_queue.qsize() == 0):
            time.sleep(0.01)
        return


if __name__ == '__main__':
    # import random
    def test(n):
        s = '%d\t开始运行\n' % n
        print(s, end='')
        for i in range(int(n)):
            # print(n)
            time.sleep(0.1)
        s = '%d\t运行完毕**********\n' % n
        print(s, end='')
        return n


    tp = ThreadingPool(10)
    for i in range(20, 1, -1):
        temp = i
        tp.append(target=test, args=(temp, ), name=str(temp))
    tp.close()
    tp.join()
    print(temp, " 搞定咯\n\n")

    pass
