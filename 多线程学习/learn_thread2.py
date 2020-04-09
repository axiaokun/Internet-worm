import threading
import time


class write_thread(threading.Thread):  # 继承threading.Thread类
    def run(self):  # 重写run函数，记得要运行的代码一定要放在run里面
        for _ in range(3):
            print('writting %s\n' % threading.current_thread())
            time.sleep(1)


class draw_thread(threading.Thread):
    def run(self):
        for _ in range(3):
            print('drawing %s\n' % threading.current_thread())
            time.sleep(1)


def main():
    t1 = write_thread()
    t2 = draw_thread()

    t1.start()
    t2.start()


if __name__ == '__main__':
    main()