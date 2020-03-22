import pymysql
from urllib import request
from urllib import error
from bs4 import BeautifulSoup


def htmls(arg):
    # 请求头
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',}
    # 资源定位符
    url = 'https://movie.douban.com/top250?start='+str(arg)+'&filter='
    resp = request.Request(url, headers=headers)  # 请求
    try:
        response = request.urlopen(resp)
    except error.URLError as e:
        print(e.reason)
    html = response.read().decode('UTF-8')
    return html


def parse(html, cur, connect_obj):
    """对html解析 并且存入到mysql"""
    data = BeautifulSoup(html, 'lxml')
    text = data.find('ol', {'class': 'grid_view'})
    top250 = text.find_all('li')
    for context in top250:  # 获取各个部分的内容存入mysql中
        info = context.find('p', {'class': ''}).text
        tp = info.strip().split("/")  # 最后一个元素为类别
        director = ''.join(tp).split("主")  # 头元素为导演
        tp_movie = tp[-1]

        #  添加数据
        sql = "insert into movie VALUES(%s,%s,%s,%s,%s,%s,%s)"
        count = cur.execute(sql, [int(context.find('em', {'class': ''}).string),
                                  str(context.find('span', {'class': 'title'}).string),
                                  str(context.find('a').find('img')['src']),
                                  str(context.find('span', {'class': 'rating_num'}).string),
                                  director[0], tp_movie,
                                  str(context.find('span', {'class': 'inq'}).string)])  # 执行mysql语句
        connect_obj.commit()  # 提交修改


def main(database, password):
    # 与数据库建立联系
    connect_obj = pymysql.connect(host='localhost', user='root', password=password, database=database, port=3306)
    cur = connect_obj.cursor()  # 获取游标
    for i in range(0, 100, 25):  # 获取前四页的内容
        parse(htmls(i), cur, connect_obj)
    cur.close()
    connect_obj.close()


if __name__ == "__main__":
    database = input("请输入mysql库名称：")
    password = input("请输入mysql密码：")
    main(database, password)
