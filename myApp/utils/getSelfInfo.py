from .getPublicData import *
from myApp.models import User


def getPageData():
    jobs = getAllJobInfo()
    jobsType = {}
    for i in jobs:
        if jobsType.get(i.type, -1) == -1:
            jobsType[i.type] = 1
        else:
            jobsType[i.type] += 1

    return list(educations.keys()), workExperience, list(jobsType.keys())


def changeSelfInfo(newInfo, fileInfo):
    user = User.objects.get(username=newInfo.get('username'))
    user.educational = newInfo.get('educational')
    user.workExpirence = newInfo.get('workExperience')
    user.address = newInfo.get('address')
    user.work = newInfo.get('work')
    if fileInfo.get('avatar') != None:
        user.avatar = fileInfo.get('avatar')
    user.save()
