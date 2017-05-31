#encoding=utf-8

import MySQLdb
from DBUtils.PooledDB import PooledDB

#5为连接池里的最少连接数
reportPool = PooledDB(MySQLdb,5,host='',user='',passwd='',db='',port=3306, charset="utf8")

#根据schoolId 与 分表策略算出 具体分表
def getTableNumBySchoolId(schoolId):
    return schoolId % 10 + 1

#根据 schoolId 和 examId 从 exam_result 表中获取学生上传的成绩的组织信息，返回学生信息字典
def getStudentInfoNowByStudentIds(schoolId,subjectBaseId,studentIds):

    if isinstance(studentIds,list) is False or len(studentIds) < 1:
        print "getStudentInfoNowByStudentIds 所接受的数据类型不是 list"
        return

    reportConn = reportPool.connection()
    cur = reportConn.cursor()

    tableNum = getTableNumBySchoolId(schoolId)
    SQL = "select examId,studentId,clzssId,subjectId,createTime from exam_result_" + str(tableNum) + " where schoolId =" + str(schoolId) + " and examId =" + str(examId) + ";"

    result = cur.execute(SQL)

    dataInfo = cur.fetchmany(result)

    dict = {}
    for i in dataInfo:
        studentId = i[1]
        clzssId = i[2]
        if dict.get(studentId,False):
            listArr = dict[studentId]
            flag = False
            for listi in listArr:
                if listi[2] == clzssId:
                    flag = True
                    break
            if flag:
                continue
        else:
            dict[studentId] = []

        listii = dict[studentId]
        listii.append([i[0],i[1],i[2],i[3],i[4]])
        dict[studentId] = listii

    cur.close()
    reportConn.close()
    return dict

#
# dict = getStudentExamInfoByExamId(112331,1999)
#
# print "keys 是" + str(dict.keys())
# print "key 的数目是" + str(len(dict.keys()))
# print dict
#
# for key in dict:
#     if len(dict[key]) > 1:
#         print "调班学生是：" + str(key)