from .getPublicData import *
from myApp.models import JobInfo
import json


def getPageData():
    job = []
    jobs = getAllJobInfo()
    for i in jobs:
        job.append(i.type)
    return list(set(job))


def getTechData():
    jobs = JobInfo.objects.all()
    workTagData = {}
    for job in jobs:
        workTag = json.loads(job.workTag)
        for w in workTag:
            if not w:
                break
            if workTagData.get(w, -1) == -1:
                workTagData[w] = 1
            else:
                workTagData[w] += 1

    result = sorted(workTagData.items(), key=lambda x: x[1], reverse=True)[:20]
    techRow = []
    techColumn = []
    for k, v in result:
        techRow.append(k)
        techColumn.append(v)

    return techRow, techColumn


def getCompanyStatusData():
    jobs = getAllJobInfo()
    statusData = {}
    for job in jobs:
        if statusData.get(job.companyStatus, -1) == -1:
            statusData[job.companyStatus] = 1
        else:
            statusData[job.companyStatus] += 1

    result = []
    for k, v in statusData.items():
        result.append({
            'name': k,
            'value': v
        })

    return result
