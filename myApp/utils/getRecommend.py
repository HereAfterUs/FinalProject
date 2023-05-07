import json
from collections import Counter
from myApp.models import JobInfo, User
from .getPublicData import *


def recommendType(uname):
    # ('北京', 265), ('深圳', 255), ('上海', 200), ('杭州', 154), ('广州', 91),('成都', 80)
    # 保证岗位一致
    # 学历和工作经验大于等于岗位要求
    # 权重的设计：address salary companyTags
    # address：是否与自己的意向城市一致
    # salary：与所处城市的最低薪资的平均值进行差值 划梯度赋分

    userInfo = User.objects.get(username=uname)
    # 总分数
    typeGrade = {}
    # 城市分数
    addGrade = {}
    # 薪资分数
    salGrade = {}

    jobs = JobInfo.objects.all()
    test = []
    typeSal1 = []
    typeSal2 = []
    typeSal3 = []
    typeSal4 = []
    typeSal5 = []
    typeSal6 = []
    for i in jobs:
        if i.type == userInfo.work and i.practice == 0 and educations[i.educational] >= educations[userInfo.educational] and workExperienceA[i.workExperience] <= workExperienceA[userInfo.workExpirence]:
            # 平均薪资
            if i.address == '北京':
                Sal = json.loads(i.salary)[0]
                typeSal1.append(Sal)

            if i.address == '深圳':
                Sal = json.loads(i.salary)[0]
                typeSal2.append(Sal)

            if i.address == '上海':
                Sal = json.loads(i.salary)[0]
                typeSal3.append(Sal)

            if i.address == '杭州':
                Sal = json.loads(i.salary)[0]
                typeSal4.append(Sal)

            if i.address == '广州':
                Sal = json.loads(i.salary)[0]
                typeSal5.append(Sal)

            if i.address == '成都':
                Sal = json.loads(i.salary)[0]
                typeSal6.append(Sal)

            # 最低薪资平均值
            salary = json.loads(i.salary)[0]
            test.append(salary)

    # 每个城市的最低平均薪资
    if len(typeSal1) != 0:
        Jsal = round(sum(typeSal1) / len(typeSal1))
    if len(typeSal2) != 0:
        Zsal = round(sum(typeSal2) / len(typeSal2))
    if len(typeSal3) != 0:
        Ssal = round(sum(typeSal3) / len(typeSal3))
    if len(typeSal4) != 0:
        Hsal = round(sum(typeSal4) / len(typeSal4))
    if len(typeSal5) != 0:
        Gsal = round(sum(typeSal5) / len(typeSal5))
    if len(typeSal6) != 0:
        Csal = round(sum(typeSal6) / len(typeSal6))

    addSal1 = {}
    addSal2 = {}
    addSal3 = {}
    addSal4 = {}
    addSal5 = {}
    addSal6 = {}

    # 赋值
    for i in jobs:
        if i.type == userInfo.work and i.practice == 0 and educations[i.educational] >= educations[
            userInfo.educational] and workExperienceA[i.workExperience] <= workExperienceA[userInfo.workExpirence]:
            # 初始化分数
            typeGrade[i.id] = 50
            # 意向城市赋值
            if i.address == userInfo.address:
                addGrade[i.id] = 20
            # 薪资赋值
            if i.address == '北京':
                addSal1[i.id] = (json.loads(i.salary)[0] - Jsal) / 100

            if i.address == '深圳':
                addSal2[i.id] = (json.loads(i.salary)[0] - Zsal) / 100

            if i.address == '上海':
                addSal3[i.id] = (json.loads(i.salary)[0] - Ssal) / 100

            if i.address == '杭州':
                addSal4[i.id] = (json.loads(i.salary)[0] - Hsal) / 100

            if i.address == '广州':
                addSal5[i.id] = (json.loads(i.salary)[0] - Gsal) / 100

            if i.address == '成都':
                addSal6[i.id] = (json.loads(i.salary)[0] - Csal) / 100

    test1 = {}
    test2 = {}
    test3 = {}
    test4 = {}
    test5 = {}
    test6 = {}
    test7 = {}
    for key in list(set(addSal1) | set(addSal2)):
        if addSal1.get(key) and addSal2.get(key):
            test1.update({key: addSal1.get(key) + addSal2.get(key)})
        else:
            test1.update({key: addSal1.get(key) or addSal2.get(key)})

    for key in list(set(addSal3) | set(addSal4)):
        if addSal3.get(key) and addSal4.get(key):
            test2.update({key: addSal3.get(key) + addSal4.get(key)})
        else:
            test2.update({key: addSal3.get(key) or addSal4.get(key)})

    for key in list(set(addSal5) | set(addSal6)):
        if addSal5.get(key) and addSal6.get(key):
            test3.update({key: addSal5.get(key) + addSal6.get(key)})
        else:
            test3.update({key: addSal5.get(key) or addSal6.get(key)})

    for key in list(set(typeGrade) | set(addGrade)):
        if typeGrade.get(key) and addGrade.get(key):
            test4.update({key: typeGrade.get(key) + addGrade.get(key)})
        else:
            test4.update({key: typeGrade.get(key) or addGrade.get(key)})

    for key in list(set(test1) | set(test2)):
        if test1.get(key) and test2.get(key):
            test5.update({key: test1.get(key) + test2.get(key)})
        else:
            test5.update({key: test1.get(key) or test2.get(key)})

    for key in list(set(test3) | set(test4)):
        if test3.get(key) and test4.get(key):
            test6.update({key: test3.get(key) + test4.get(key)})
        else:
            test6.update({key: test3.get(key) or test4.get(key)})

    for key in list(set(test5) | set(test6)):
        if test5.get(key) and test6.get(key):
            test7.update({key: test5.get(key) + test6.get(key)})
        else:
            test7.update({key: test5.get(key) or test6.get(key)})

    test7 = sorted(test7.items(), key=lambda x: x[1], reverse=True)[:3]
    type1 = test7[0]
    type2 = test7[1]
    type3 = test7[2]
    type1 = type1[0]
    type2 = type2[0]
    type3 = type3[0]

    return type1, type2, type3


def getTableData():
    jobs = getAllJobInfo()
    for i in jobs:
        i.workTag = '/'.join(json.loads(i.workTag))
        if i.companyTags != "无":
            i.companyTags = '/'.join(json.loads(i.companyTags))
        if i.companyPeople == '[0, 10000]':
            i.companyPeople = '10000人以上'
        else:
            i.companyPeople = json.loads(i.companyPeople)
            i.companyPeople = list(map(lambda x: str(x) + '人', i.companyPeople))
            i.companyPeople = '-'.join(i.companyPeople)
        i.salary = json.loads(i.salary)
    return jobs
