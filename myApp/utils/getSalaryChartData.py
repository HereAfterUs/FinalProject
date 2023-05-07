from .getPublicData import *
from myApp.models import JobInfo

import json


# 获取学历和经验
def getPageData():
    return list(educations.keys()), workExperience


# 2107
def getBarData(defaultEducation, defaultWorkExperience):

    salaryList = ['0-10K', '10-20K', '20-30K', '30k以上']
    # 判断两个下拉框条件
    if defaultEducation == '不限' and defaultWorkExperience == '不限':
        jobs = JobInfo.objects.all()
    elif defaultWorkExperience == '不限':
        jobs = JobInfo.objects.filter(educational=defaultEducation)
    elif defaultEducation == '不限':
        jobs = JobInfo.objects.filter(workExperience=defaultWorkExperience)
    else:
        jobs = JobInfo.objects.filter(educational=defaultEducation, workExperience=defaultWorkExperience)

    jobsType = {}
    for j in jobs:
        if j.practice == 0:
            if jobsType.get(j.type, -1) == -1:
                jobsType[j.type] = [json.loads(j.salary)[1]]
            else:
                jobsType[j.type].append(json.loads(j.salary)[1])
    barData = {}
    for k, v in jobsType.items():
        if not barData.get(k, 0):
            barData[k] = [0 for x in range(4)]
        for i in v:
            s = i / 1000
            if s < 10:
                barData[k][0] += 1
            elif 10 <= s < 20:
                barData[k][1] += 1
            elif 20 <= s < 30:
                barData[k][2] += 1
            else:
                barData[k][3] += 1

    legends = list(barData.keys())
    if len(legends) == 0:
        legends = None
    return salaryList, barData, legends


def roseData():
    # gt是大于的意思
    jobs = JobInfo.objects.filter(salaryMonth__gt=0)
    data = {}
    for j in jobs:
        x = str(j.salaryMonth) + '薪'
        if data.get(x, -1) == -1:
            data[x] = 1
        else:
            data[x] += 1
    result = []
    for k, v in data.items():
        result.append({
            'name': k,
            'value': v
        })
    return list(data.keys()), result
