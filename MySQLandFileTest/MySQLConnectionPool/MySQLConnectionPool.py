#encoding=utf-8

import MySQLdb
from DBUtils.PooledDB import PooledDB
# pool = PooledDB(MySQLdb,5,host='localhost',user='root',passwd='123456',db='fzexam',port=3306, charset="utf8") #5为连接池里的最少连接数

#account 连接池
accountPool = PooledDB(MySQLdb,5,host='',user='',passwd='',db='',port=0, charset="utf8")

#report 连接池
reportPool = PooledDB(MySQLdb,5,host='',user='',passwd='',db='',port=0, charset="utf8")