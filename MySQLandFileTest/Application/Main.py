#encoding=utf-8

import os
import sys
from MySQLandFileTest.MySQLConnectionPool.AccountConnectionPool import *
from MySQLandFileTest.MySQLConnectionPool.ReportConnectionPool import *

examId = 113181
schoolId = 1999
year = 2016
subjectBaseId = 0

#根据 schoolId 和 examId 从 exam_result 表中获取学生上传的成绩的组织信息，返回学生信息字典
studentInfoExamResult = getStudentExamInfoByExamId(examId,schoolId)
print studentInfoExamResult
subjectBaseId = studentInfoExamResult[studentInfoExamResult.keys()[0]][0][5]

if not studentInfoExamResult:
    print "信息错误，未获取到数据"
    sys.exit()


#获取需要转为缺考的学生班级信息
studentExamResultToSetStatusTo5 = getStudentExamResultToSetStatusTo5(studentInfoExamResult)
print studentExamResultToSetStatusTo5

if not studentExamResultToSetStatusTo5:
    print "没有学生在多个班中个上传过成绩"
else:
    # 将需要置缺考的学生成绩 status 置为 5
    print ""
    print ""
    print "=================================================================置缺考开始========================================================================="
    updateExamResultStatusTo5(schoolId, examId, studentExamResultToSetStatusTo5)
    print "=================================================================置缺考结束========================================================================="
    print ""
    print ""


#根据 schoolId 和 examId 从 exam_result 表中获取学生上传的成绩的组织信息，返回学生信息字典
studentIds = studentInfoExamResult.keys()
studentInfoNow = getStudentInfoNowByStudentIds(schoolId,subjectBaseId,year,studentIds)
print studentInfoNow

if not studentInfoNow:
    print "参数错误，未获取到学生信息"
    sys.exit()


# 获取需要需要保留的exam_result 中的学生班级信息
# item like {1250261L: 32543L}
studentExamResultClzssInfo = getStudentExamResultClzssInfo(studentInfoExamResult)
print studentExamResultClzssInfo

if not studentExamResultClzssInfo:
    print "参数错误，学生考试时的班级信息"
    sys.exit()


#将需要置缺考的学生成绩 status 置为 5
print ""
print ""
print ""
print ""
print "==========================================================================================================================================================="
print "=================================================================调班学生调整数据开始========================================================================="
updateExamResultStudentInfo(schoolId,examId,studentInfoNow,studentExamResultClzssInfo)
print "=================================================================调班学生调整数据结束========================================================================="
print "==========================================================================================================================================================="




