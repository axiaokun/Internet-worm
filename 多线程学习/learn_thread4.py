"""
本次学习：
多线程中生成者和消费者模式
"""


import threading
import time
import random

money_sum = 1000
glock = threading.Lock()


class Produce(threading.Thread):
    def run(self):
        global money_sum
        while True:
            money = random.randint(100, 1000)
            glock.acquire()
            money_sum += money
            print('%s生产了%d元钱，剩余%d多少元钱' % (threading.current_thread(), money, money_sum))
            glock.release()
            time.sleep(1)


class Consumer(threading.Thread):
    def run(self):
        global money_sum
        while True:
            money = random.randint(100, 1000)
            glock.acquire()
            if money_sum > money:
                money_sum -= money
                print('%s消费了%d元钱，剩余%d多少元钱' % (threading.current_thread(), money, money_sum))
            glock.release()
            time.sleep(1)


def main():
    for i in range(3):
        t = Consumer(name='消费者线程%d' % i)
        t.start()

    for i in range(5):
        t = Produce(name='生产者线程%d' % i)
        t.start()


if __name__ == '__main__':
    main()
