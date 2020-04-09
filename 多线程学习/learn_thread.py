import threading
import time


def write():
    for i in range(3):
        print('正咋书写%s\n'% threading.current_thread())  # 打印该线程的名称
        time.sleep(1)


def draw():
    for i in range(3):
        print('正在绘画%s\n'% threading.current_thread())
        time.sleep(1)


def main():
    t1 = threading.Thread(target=write)
    t2 = threading.Thread(target=draw)

    t1.start()
    t2.start()

    # 这里有三个线程，包括有main主线程，还有t1，t2这两个线程
    print(threading.enumerate())  # 查看所有的线程


if __name__ == '__main__':
    main()