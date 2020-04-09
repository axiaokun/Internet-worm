# encode: utf-8
"""
队列安全
队列中实现了锁原语，要么不做，要么做完
使用队列可以实现线程中的同步
队列get和put默认不满足条件时自动堵塞
"""
from queue import Queue
import time
import threading


# for i in range(4):
#     q.put(i)
#
# print(q.full())  # 判断队列是否满了
# print(q.qsize())  # 队列大小
#
# for i in range(4):
#     print(q.get())  # 获取队列头部
#
# print(q.empty())  # 是否为空


def set_value(q):
    index = 0
    while True:
        q.put(index)
        index += 1
        time.sleep(3)  # 这遍每隔三秒才会生产一个数字


def get_value(q):
    while True:
        print(q.get())  # 利用队列来实现线程间的同步，如果队列中没有数值，那么这一步就会堵塞，直到队列中有数值为止


if __name__ == '__main__':
    q = Queue(4)
    t1 = threading.Thread(target=set_value, args=[q])
    t2 = threading.Thread(target=get_value, args=[q])

    t1.start()
    t2.start()
