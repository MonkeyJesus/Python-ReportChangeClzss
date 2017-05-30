#encoding=utf-8

import MySQLdb
from DBUtils.PooledDB import PooledDB

#5为连接池里的最少连接数
reportPool = PooledDB(MySQLdb,5,host='114.215.111.29',user='yjw0223',passwd='f9a<)6hh>0pP',db='fzreport',port=3314, charset="utf8")

#根据schoolId 与 分表策略算出 具体分表
def getTableNumBySchoolId(schoolId):
    return schoolId % 10 + 1

#根据 schoolId 和 examId 从 exam_result 表中获取学生上传的成绩的组织信息，返回学生信息字典
def getStudentExamInfoByExamId(examId,schoolId):

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

#根据条件将多余的成绩置缺考
def updateExamResultStatusTo5(schoolId,examId,studentInfoMap):

    #记录总影响的条数
    row_num = 0

    #判断 studentInfoMap 的数据类型
    if isinstance(studentInfoMap,dict):
        pass
    else:
        print "studentInfoMap 不是传的 字典 类型"
        return

    reportConn = reportPool.connection()
    cur = reportConn.cursor()

    SQL = "update exam_result_" + str(getTableNumBySchoolId(schoolId)) + " set status = 5 where schoolId = " + str(schoolId) + " and examId = " + str(examId)

    for studentId in studentInfoMap.keys():
        if studentInfoMap.get(studentId,False):
            pass
        else:
            print "studentInfoMap 的value 不是 列表"
            continue

        clzssIds = studentInfoMap.get(studentId)
        if isinstance(clzssIds,list) is False:
            continue

        for clzssId in clzssIds:
            SQL2 = SQL + " and studentId = " + str(studentId) + " and clzssId = " + str(clzssId)
            try:
                print SQL2
                i = cur.execute(SQL2)
                row_num += i
                reportConn.commit()
            except:
                reportConn.rollback()

    print row_num
    #关闭游标
    cur.close()
    #关闭连接
    reportConn.close()


def updateExamResultStudentInfo(schoolId,examId,studentInfoBAccountOrg,studentInfoExamResult):
    # 判断 studentInfoMap 的数据类型
    if isinstance(studentInfoBAccountOrg, dict) is False or isinstance(studentInfoExamResult, dict) is False:
        print "studentInfo 不是传的 字典 类型"
        return

    if studentInfoBAccountOrg.keys() != studentInfoExamResult.keys():
        print "BAccountOrg 中的学生个数与 ExamResult 中的学生不同"
        return

    SQL = "update exam_result_" + str(getTableNumBySchoolId(schoolId)) + " set clzssId = %d , clzssName = '%s' , subjectId = %d , subjectName = '%s' where schoolId = %d and examId = %d" \
                                                                         " and studentId = %d and clzssId = %d"

    for studentId in studentInfoExamResult.keys():
        if isinstance(studentInfoBAccountOrg[studentId],list) is False or len(studentInfoBAccountOrg[studentId]) < 4:
            continue
        nowClzssId = studentInfoBAccountOrg[studentId][0]
        nowClzssName = studentInfoBAccountOrg[studentId][1]
        nowSubjectId = studentInfoBAccountOrg[studentId][2]
        nowSubjectName = studentInfoBAccountOrg[studentId][3]
        oldClzssId = studentInfoExamResult[studentId]

        SQL = SQL % (nowClzssId,nowClzssName,nowSubjectId,nowSubjectName,schoolId,examId,studentId,oldClzssId)

        print SQL
    return

studentInfoBAccountOrg = {1250311:[32553,"1班" ,123 ,"数学"]}
studentInfoExamResult = {1250311:111111111}

print studentInfoExamResult.keys()

updateExamResultStudentInfo(1999,112331,studentInfoBAccountOrg,studentInfoExamResult)

# updateExamResultStatusTo5(1999,112331,studentInfoMap)



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