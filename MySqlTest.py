#coding=utf-8
#!/usr/bin/python

import MySQLdb

#打开数据库链接
db = MySQLdb.connect('localhost','root','123456','fzexam');

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("select id from exam limit 1")

# 使用 fetchone() 方法获取一条数据库。
data = cursor.fetchone()

print "Database version : %s " % data

# 关闭数据库连接
db.close()