from myApp.models import User, JobInfo

monthList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"]

educations = {"博士": 1, "硕士": 2, "本科": 3, "大专": 4, "高中": 5, "中专/中技": 6, "初中及以下": 7, "学历不限": 8}
workExperience = ['在校/应届', '经验不限', '1年以内', '1-3年', '3-5年', '5-10年', '10年以上']
workExperienceA = {"在校/应届": 2, "经验不限": 1, "1年以内": 3, "1-3年": 4, "3-5年": 5, "5-10年": 6, "10年以上": 7}
salaryList = ['0-10K', '10-20K', '20-30K', '30k以上']
companyPeople = ['50', '100', '500', '1000', '10000', '>10000']
hotCity = ['北京', '上海', '深圳', '成都', '重庆', '广州', '西安', '天津']
typeList = ['Java开发', '前端', '.NET', 'Linux', 'Go', 'Python', 'PHP', '嵌入式', '软件测试', '全栈工程师']


def getAllUser():
    return User.objects.all()


def getAllJobInfo():
    return JobInfo.objects.all()
