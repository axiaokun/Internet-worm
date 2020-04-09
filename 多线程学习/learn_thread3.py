"""
这种情况是没有加锁但是在这个进程中的多个线程会用到这个进程里面的全局变量
而且由于全局变量在同个进程中是共享的，所以但他们同时进行的时候可能只是同时
对一个相同的值加一，结果一样。也就导致了多次进行加一后结果不像我们预想的那样
"""

import threading
#
# VALUE = 0
#
#
# def add_value():
#     global VALUE
#     for _ in range(1000000):
#         VALUE += 1
#     print(VALUE, end='\n')
#
#
# def main():
#     for _ in range(2):
#         ti = threading.Thread(target=add_value)
#         ti.start()
#
#
# if __name__ == '__main__':
#     main()


"""
下面是加锁后的代码
"""

VALUE = 0
glock = threading.Lock()


def add_value():
    global VALUE
    glock.acquire()
    for _ in range(1000000):
        VALUE += 1
    glock.release()
    print(VALUE, end='\n')


def main():
    for _ in range(2):
        ti = threading.Thread(target=add_value)
        ti.start()


if __name__ == '__main__':
    main()
