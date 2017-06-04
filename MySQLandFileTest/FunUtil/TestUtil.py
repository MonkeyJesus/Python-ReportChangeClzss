#encoding=utf-8

#根据schoolId 与 分表策略算出 具体分表
def getTableNumBySchoolId(schoolId):
    return schoolId % 10 + 1

