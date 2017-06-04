#encoding=utf-8

from MySQLandFileTest.FunUtil.TestUtil import *

import MySQLdb
from DBUtils.PooledDB import PooledDB
from MySQLConnectionPool import accountPool

#根据 schoolId 和 examId 从 exam_result 表中获取学生上传的成绩的组织信息，返回学生信息字典
def getStudentInfoNowByStudentIds(schoolId,subjectBaseId,year,studentIds):

    if isinstance(studentIds,list) is False or len(studentIds) < 1:
        print "getStudentInfoNowByStudentIds 所接受的数据类型不是 list"
        return

    accountConn = accountPool.connection()
    cur = accountConn.cursor()

    tableNum = getTableNumBySchoolId(schoolId)
    SQL = "select accountId,clzssId,clzssName,subjectId,subjectName from b_account_org_" + str(tableNum) + " where schoolId = %d " \
            "and subjectBaseId = %d and year = %d and accountId in (%s) group by accountId;" % (schoolId,subjectBaseId,year,",".join(map(str,studentIds)))

    print SQL

    result = cur.execute(SQL)
    dataInfo = cur.fetchmany(result)

    # print len(dataInfo)

    dictStudentNow = {}
    if len(dataInfo) > 0:
        for dataItem in dataInfo:
            dictStudentNow[dataItem[0]] = [dataItem[1],dataItem[2],dataItem[3],dataItem[4]]

    cur.close()
    accountConn.close()
    return dictStudentNow

#
# dictResult = getStudentInfoNowByStudentIds(1999,1,2016,[1250311])
# print "结果：" + str(dictResult)
#
# print "keys 是" + str(dict.keys())
# print "key 的数目是" + str(len(dict.keys()))
# print dict
#
# for key in dict:
#     if len(dict[key]) > 1:
#         print "调班学生是：" + str(key)