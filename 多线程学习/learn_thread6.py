# encode: utf-8
"""
同步下载表情包
"""

import requests
from lxml import etree
from urllib import request
import os
import re


def parse_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    response = requests.get(url, headers)
    test = response.text
    html = etree.HTML(test)
    imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
    for img in imgs:
        img_url = img.get('data-original')
        alt = img.get('alt')
        alt = re.sub(r'[\?？\.，。！!●/]', '', alt)
        suffix = os.path.splitext(img_url)[1]
        filename = alt + suffix
        request.urlretrieve(img_url, 'images/'+filename)


def main():
    for x in range(101):
        url = "https://www.doutula.com/photo/list/?page=%d" % x
        parse_page(url)


if __name__ == '__main__':
    main()
