# encode: utf-8
"""
异步下载表情包
使用生产者消费者模式

生产者：生成图片地址url

消费者：下载图片

本次知识点：

1. 线程安全队列
    这个主要是由于在一个进程中的资源是可以被这个进程中的所有线程共享的，而线程的快慢又是不一致的。因此无法保证他们会在上面时候同时
    访问同一个资源，

    所以我们需要一种操作：原子操作
        这种操作不会被线程打断，要么不执行，一旦执行就会一直执行到结束中间不会切换别的线程。

    操作有二：
        1.加锁
        2.使用队列

    python中的queue队列属于线程安全，底部封装锁。所也就是当我们需要独占这块资源的时候就可以把它锁住，这样它就不会被其他线程占用，当
    我们使用完后就可以释放锁，使得其他线程可以使用。

2. 消费者生产者模式

    生产者就是生产数据的线程，消费者就是处理数据的线程

    一般流程是生产者生产数据，然后将这些数据丢到缓冲区，消费者从缓冲区取出数据进行处理。一般使用阻塞队列充当缓冲区来进行两者间的通讯

    优点：
        1.解耦
        减少两者之间依赖性

        2.支持并发
        如果两者中其中一个速度慢了，那么其中一个仍然可以进行，只要缓冲区还ok
"""

import requests
from lxml import etree
from urllib import request
from queue import Queue
import threading
import os
import re


class Procuder(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }

    def __init__(self, page_queue, image_queue, *args, **kwargs):
        super(Procuder, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.image_queue = image_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self, url):
        response = requests.get(url, self.headers)
        test = response.text
        html = etree.HTML(test)
        imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")  # 使用xpath解析
        for img in imgs:
            img_url = img.get('data-original')
            alt = img.get('alt')
            alt = re.sub(r'[\?？\.，。！!●/]', '', alt)  # 过滤掉表情包标签中一些符号
            suffix = os.path.splitext(img_url)[1]  # 获取后缀
            filename = alt + suffix  # 将标签和后缀作为文件名
            self.image_queue.put((img_url, filename))  # 将数据传入队列


class Consumer(threading.Thread):
    def __init__(self, page_queue, image_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.image_queue = image_queue

    def run(self):
        while True:
            if self.page_queue.empty() and self.image_queue.empty():
                break
            img_url, filename = self.image_queue.get()  # 从队列中取出图片url和文件名称
            request.urlretrieve(img_url, 'images/'+filename)  # 下载图片
            print(filename+'下载完成')


def main():
    page_queue = Queue(100)
    image_queue = Queue(1000)
    for x in range(100):
        url = "https://www.doutula.com/photo/list/?page=%d" % x
        page_queue.put(url)

    for x in range(5):
        t = Procuder(page_queue, image_queue)
        t.start()

    for x in range(5):
        t = Consumer(page_queue, image_queue)
        t.start()


if __name__ == '__main__':
    main()

