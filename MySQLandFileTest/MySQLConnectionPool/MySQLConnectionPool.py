#encoding=utf-8

import MySQLdb
from DBUtils.PooledDB import PooledDB
pool = PooledDB(MySQLdb,5,host='localhost',user='root',passwd='123456',db='fzexam',port=3306, charset="utf8") #5为连接池里的最少连接数

conn = pool.connection()  #以后每次需要数据库连接就是用connection（）函数获取连接就好了
cur=conn.cursor()
SQL="select * from exam"
r=cur.execute(SQL)
#r=cur.fetchall()

#print r

dataInfo = cur.fetchmany(r)

dict = {}

for i in dataInfo:

    dict[i[0]] = i[1]
    print i[0]


print dict
print dict[1412043]

cur.close()
conn.close()