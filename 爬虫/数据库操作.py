# import pymysql
#
# # 与数据库建立连接
# connect_obj = pymysql.connect(host='localhost', user='root', password='your password', database='your database', port=3306)
# cur = connect_obj.cursor()  # 获取游标
#
# #  添加数据
# sql = "insert into student VALUES(%s,%s,%s,%s)"
# count = cur.execute(sql, [0, '马冬雪', 0, '98.8'])  # 执行mysql语句
# connect_obj.commit()  # 数据修改时，一定要有这句话
# print('成功插入', count, '条数据')
#
# #  删除数据
# sql = "DELETE FROM student WHERE id = 2 "
# count = cur.execute(sql)  # 执行mysql语句
# connect_obj.commit()  # 数据修改时，一定要有这句话
# print('成功删除',count,'条数据')
#
# # 更新数据
# sql = "UPDATE student SET id = 2 WHERE id = 3 "
# count = cur.execute(sql)  # 执行mysql语句
# connect_obj.commit()  # 数据修改时，一定要有这句话
# print('成功修改',count,'条数据')
#
#
# sql = 'select * from student'
# count = cur.execute(sql)  # 执行mysql语句
# print('共查出', count, '条数据')
# ret = cur.fetchall()  # 获取结果中的所有行
#
#
# for i in ret:
#     print(i)
#
# # 关闭连接
# cur.close()
# connect_obj.close()







