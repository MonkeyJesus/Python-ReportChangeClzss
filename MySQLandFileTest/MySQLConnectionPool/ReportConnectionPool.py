#encoding=utf-8

import MySQLdb

from DBUtils.PooledDB import PooledDB
from MySQLandFileTest.FunUtil.TestUtil import *
from MySQLConnectionPool import reportPool
from datetime import datetime

#根据 schoolId 和 examId 从 exam_result 表中获取学生上传的成绩的组织信息，返回学生信息字典
def getStudentExamInfoByExamId(examId,schoolId):

    reportConn = reportPool.connection()
    cur = reportConn.cursor()

    tableNum = getTableNumBySchoolId(schoolId)
    SQL = "select examId,studentId,clzssId,subjectId,createTime,subjectBaseId from exam_result_" + str(tableNum) + " where schoolId =" + str(schoolId) + " and examId =" + str(examId) + ";"

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
        listii.append([i[0],i[1],i[2],i[3],i[4],i[5]])
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

    #获取数据库链接
    reportConn = reportPool.connection()
    #获取游标
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
            print SQL2
            # try:
            #     print SQL2
            #     i = cur.execute(SQL2)
            #     row_num += i
            #     reportConn.commit()
            # except:
            #     reportConn.rollback()

    print "updateExamResultStatusTo5 此次共更新记录数：" + str(row_num)
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

    # 获取数据库链接
    reportConn = reportPool.connection()
    # 获取游标
    cur = reportConn.cursor()

    # 记录总影响的条数
    row_num = 0

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

        if oldClzssId == nowClzssId:
            continue

        print SQL % (nowClzssId,nowClzssName,nowSubjectId,nowSubjectName,schoolId,examId,studentId,oldClzssId)


        # try:
        #     i = cur.execute(SQL % (nowClzssId,nowClzssName,nowSubjectId,nowSubjectName,schoolId,examId,studentId,oldClzssId))
        #     row_num += i
        #     reportConn.commit()
        # except:
        #     #出异常回归
        #     reportConn.rollback()

    cur.close
    reportConn.close()
    return


#比较函数
#item like [113181L, 1250261L, 32546L, 68780L, datetime.datetime(2016, 10, 20, 9, 56, 35)]
def sortDateTime(l1,l2):
    if l1[4] > l2[4]:
        return -1
    elif l1[4] < l2[4]:
        return 1
    else:
        return 0

#获取需要置为缺考的学生信息
#item like {1250261L: [32543L, 32548L]}
def getStudentExamResultToSetStatusTo5(studentExamResultDict):

    returnDict = {}

    if isinstance(studentExamResultDict,dict) is False or len(studentExamResultDict.keys()) < 1:
        return

    for studentId in studentExamResultDict.keys():
        infoList = studentExamResultDict[studentId]
        if isinstance(infoList,list) is False or len(infoList) < 1:
            continue

        if len(infoList) > 1:
            # print "重复班级：" + str(infoList)
            clzssIds = []

            infoList.sort(cmp=sortDateTime)
            for infoItem in infoList[1:len(infoList)]:
                clzssIds.append(infoItem[2])

            returnDict[studentId] = clzssIds

    return returnDict

# 获取需要需要保留的exam_result 中的学生班级信息
# item like {1250261L: 32543L}
def getStudentExamResultClzssInfo(studentExamResultDict):

    returnDict = {}

    if isinstance(studentExamResultDict, dict) is False or len(studentExamResultDict.keys()) < 1:
        return

    for studentId in studentExamResultDict.keys():
        infoList = studentExamResultDict[studentId]
        if isinstance(infoList, list) is False or len(infoList) < 1:
            continue

        if len(infoList) > 1:
            # print "重复班级：" + str(infoList)
            infoList.sort(cmp=sortDateTime)
        returnDict[studentId] = infoList[0][2]

    return returnDict

#
#
# studentInfoBAccountOrg = {1250311:[32553,"1班" ,123 ,"数学"]}
# studentInfoExamResult = {1250311:111111111}
#
# print studentInfoExamResult.keys()
#
# # updateExamResultStudentInfo(1999,112331,studentInfoBAccountOrg,studentInfoExamResult)
#
# resultDict = getStudentExamInfoByExamId(113181,1999)
# print resultDict
#
# print resultDict[1250304]
# print len(resultDict[1250304][0])
# print resultDict[1250304][0][4]
# print type(resultDict[1250304][0][4])
#
# resultDict2 = getStudentExamResultToSetStatusTo5(resultDict)
# print resultDict2
#
#
# #根据条件将多余的成绩置缺考
# updateExamResultStatusTo5(1999,113181,resultDict2)


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