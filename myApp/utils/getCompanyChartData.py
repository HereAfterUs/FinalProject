from myApp.models import JobInfo
import json
from .getPublicData import *


def getPageData():
    jobs = getAllJobInfo()
    typeData = []
    for i in jobs:
        typeData.append(i.type)
    return list(set(typeData))


def getCompanyBar(type):
    if type == '不限':
        jobs = JobInfo.objects.all()
    else:
        jobs = JobInfo.objects.filter(type=type)
    natureData = {}
    for i in jobs:
        if natureData.get(i.companyNature, -1) == -1:
            natureData[i.companyNature] = 1
        else:
            natureData[i.companyNature] += 1

    natureList = list(sorted(natureData.items(), key=lambda x: x[1], reverse=True))
    rowData = []
    columnData = []
    for k, v in natureList:
        rowData.append(k)
        columnData.append(v)
    return rowData, columnData


def getCompanyPie(type):
    if type == '不限':
        jobs = JobInfo.objects.all()
    else:
        jobs = JobInfo.objects.filter(type=type)
    addressData = {}
    for i in jobs:
        if addressData.get(i.address, -1) == -1:
            addressData[i.address] = 1
        else:
            addressData[i.address] += 1
    result = []
    for k, v in addressData.items():
        result.append({
            'name': k,
            'value': v
        })
    return result[:30]


def getCompanyPeople(type):
    if type == '不限':
        jobs = JobInfo.objects.all()
    else:
        jobs = JobInfo.objects.filter(type=type)

    # 取最大值
    def map_fn(item):
        item.companyPeople = json.loads(item.companyPeople)[1]
        return item

    jobs = list(map(map_fn, jobs))
    # 生成列表
    data = [0 for x in range(6)]
    for i in jobs:
        p = i.companyPeople
        if p <= 50:
            data[0] += 1
        elif p <= 100:
            data[1] += 1
        elif p <= 500:
            data[2] += 1
        elif p <= 1000:
            data[3] += 1
        elif p < 10000:
            data[4] += 1
        else:
            data[5] += 1
    return companyPeople, data
