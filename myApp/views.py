from myApp.models import JobInfo, User
from django.shortcuts import render, redirect, reverse
import hashlib
from .utils import getHomeData
from .utils import getSelfInfo
from .utils import getChangePasswordData
from .utils.error import *
from .utils import getSalaryChartData
from .utils import getHistoryTableData
from .utils import getCompanyChartData
from .utils import getEducationalChartData
from .utils import getCompanyStatusChartData
from .utils import getAddressChartData
from .utils import getRecommend
from .utils import getForecast
from django.contrib.auth import authenticate,login,logout


# name属性用于表单处理和后端
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        uname = request.POST.get('username')
        pwd = request.POST['password']
        md5 = hashlib.md5()
        md5.update(pwd.encode())
        pwd = md5.hexdigest()
        try:
            user = User.objects.get(username=uname, password=pwd)
            request.session['username'] = user.username
            return redirect('/myApp/home')
        except:
            return errorResponse(request, '用户名或密码错误')


def registry(request):
    if request.method == 'GET':
        return render(request, 'registry.html')
    else:
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        checkPwd = request.POST.get('checkPassword')

        try:
            User.objects.get(username=uname)
        except:
            if not uname or not pwd or not checkPwd:
                return errorResponse(request, '不允许为空')
            if pwd != checkPwd:
                return errorResponse(request, '两次密码不符合')
            md5 = hashlib.md5()
            md5.update(pwd.encode())
            pwd = md5.hexdigest()
            User.objects.create(username=uname, password=pwd)
            return redirect('/myApp/login')
        return errorResponse(request, '该用户已被注册')


def logOut(request):
    request.session.clear()
    return redirect('login')


def home(request):
    username = request.session.get("username")
    userInfo = User.objects.get(username=username)
    year, month, day = getHomeData.getNowTime()
    userCreateData = getHomeData.getUserCreateTime()
    top6User = getHomeData.getUserTop6()
    getHomeData.getAllTags()
    jobsLen, usersLen, educationsTop, salaryTop, addressTop, salaryMonthTop = getHomeData.getAllTags()
    tableData = getHomeData.getTableData()
    return render(request, 'index.html', {

        'tableData': tableData,
        'userInfo': userInfo,
        'dataInfo': {
            'year': year,
            "month": month,
            'day': day,
        },
        'userCreateData': userCreateData,
        'top6User': top6User,
        'tagDic': {
            'jobsLen': jobsLen,
            'usersLen': usersLen,
            'educationsTop': educationsTop,
            'salaryTop': salaryTop,
            'addressTop': addressTop,
            'salaryMonthTop': salaryMonthTop,
        }

    })


# 个人信息页面
def selfInfo(request):
    uname = request.session.get("username")
    userInfo = User.objects.get(username=uname)
    educations, workExperience, jobList = getSelfInfo.getPageData()
    if request.method == 'POST':
        getSelfInfo.changeSelfInfo(request.POST, request.FILES)
        userInfo = User.objects.get(username=uname)
    return render(request, 'selfInfo.html', {
        'userInfo': userInfo,
        'pageData': {
            'educations': educations,
            'workExperience': workExperience,
            'jobList': jobList
        }
    })


# 修改密码页
def changePassword(request):
    uname = request.session.get("username")
    userInfo = User.objects.get(username=uname)
    if request.method == 'POST':
        res = getChangePasswordData.changePassword(request.POST, userInfo)
        if res != None:
            return render(request, 'error.html', {
                'errorMsg': res
            })
        userInfo = User.objects.get(username=uname)
        # 重定向
        # logout(request)
    return render(request, 'changePassword.html', {
        'userInfo': userInfo
    })


def historyTableData(request):
    uname = request.session.get("username")
    userInfo = User.objects.get(username=uname)
    historyData = getHistoryTableData.getHistoryData(userInfo)
    return render(request, 'historyTableData.html', {
        'userInfo': userInfo,
        'historyData': historyData
    })


def addHistory(request, jobId):
    uname = request.session.get("username")
    userInfo = User.objects.get(username=uname)
    getHistoryTableData.addHistory(userInfo, jobId)
    return redirect('historyTableData')


def removeHistory(request, hisId):
    getHistoryTableData.removeHistory(hisId)
    return redirect('historyTableData')


# 薪资情况
def salary(request):
    uname = request.session.get("username")
    userInfo = User.objects.get(username=uname)

    educations, workExperience = getSalaryChartData.getPageData()
    # 下拉选项框
    defaultEducation = '不限'
    defaultWorkExperience = '不限'
    if request.GET.get("educational"):
        defaultEducation = request.GET.get("educational")
    if request.GET.get("workExperience"):
        defaultWorkExperience = request.GET.get("workExperience")

    salaryList, barData, legends = getSalaryChartData.getBarData(defaultEducation, defaultWorkExperience)
    roseData = getSalaryChartData.roseData()
    return render(request, 'salaryChart.html', {
        'userInfo': userInfo,
        'educations': educations,
        'workExperience': workExperience,
        'defaultEducation': defaultEducation,
        'defaultWorkExperience': defaultWorkExperience,
        'salaryList': salaryList,
        'barData': barData,
        'legends': legends,
        'roseData': roseData
    })


# 企业情况
def company(request):
    uname = request.session.get("username")
    userInfo = User.objects.get(username=uname)
    typeList = getCompanyChartData.getPageData()
    type = '不限'
    if request.GET.get("type"):
        type = request.GET.get("type")
    rowBarData, columnBarData = getCompanyChartData.getCompanyBar(type)
    pieData = getCompanyChartData.getCompanyPie(type)
    companyPeople, lineData = getCompanyChartData.getCompanyPeople(type)
    return render(request, 'companyChart.html', {
        'userInfo': userInfo,
        'typeList': typeList,
        'type': type,
        'rowBarData': rowBarData,
        'columnBarData': columnBarData,
        'pieData': pieData,
        'companyPeople': companyPeople,
        'lineData': lineData
    })


def educational(request):
    uname = request.session.get("username")
    userInfo = User.objects.get(username=uname)

    defaultEducation = '不限'
    if request.GET.get("educational"):
        defaultEducation = request.GET.get("educational")
    educations = getEducationalChartData.getPageData()
    workExperiences, chartDataColumnOne, chartDataColumnTwo, hasEmpty = getEducationalChartData.getExperienceLineData(
        defaultEducation)
    barDataRow, barDataColumn = getEducationalChartData.getPeopleData()
    return render(request, 'educationalChart.html', {
        "userInfo": userInfo,
        'educations': educations,
        'defaultEducation': defaultEducation,
        'workExperiences': workExperiences,
        'chartDataColumnOne': chartDataColumnOne,
        'chartDataColumnTwo': chartDataColumnTwo,
        "hasEmpty": hasEmpty,
        'barDataRow': barDataRow,
        'barDataColumn': barDataColumn
    })


def companyStatus(request):
    uname = request.session.get("username")
    userInfo = User.objects.get(username=uname)
    techRow, techColumn = getCompanyStatusChartData.getTechData()
    companyStatusData = getCompanyStatusChartData.getCompanyStatusData()
    return render(request, 'companyStatusChart.html', {
        'userInfo': userInfo,
        'techRow': techRow,
        'techColumn': techColumn,
        'companyStatusData': companyStatusData
    })


def address(request):
    uname = request.session.get("username")
    userInfo = User.objects.get(username=uname)
    defaultCity = '成都'
    if request.GET.get('city'):
        defaultCity = request.GET.get('city')
    hotCities = getAddressChartData.getPageData()
    salaryRow, salaryColumn = getAddressChartData.getSalary(defaultCity)
    companyPeopleData = getAddressChartData.companyPeopleData(defaultCity)
    educationData = getAddressChartData.getEducationData(defaultCity)
    distData = getAddressChartData.getDistData(defaultCity)
    return render(request, 'addressChart.html', {
        'userInfo': userInfo,
        'hotCities': hotCities,
        'defaultCity': defaultCity,
        'salaryRow': salaryRow,
        'salaryColumn': salaryColumn,
        'companyPeopleData': companyPeopleData,
        'educationData': educationData,
        'distData': distData
    })


def recommend(request):
    uname = request.session.get("username")
    userInfo = User.objects.get(username=uname)
    type1, type2, type3 = getRecommend.recommendType(uname)
    tableData2 = getRecommend.getTableData()
    print(type1, type2, type3)

    return render(request, 'recommendFunction.html', {
        'userInfo': userInfo,
        'type1': type1,
        'type2': type2,
        'type3': type3,
        'tableData2': tableData2
    })


def forecast(request):
    uname = request.session.get("username")
    userInfo = User.objects.get(username=uname)
    defaultType = 'Java开发'
    if request.GET.get('forecast'):
        defaultType = request.GET.get('forecast')
    workExp = request.GET.get('workExp', '')
    print(defaultType, workExp)
    types = getForecast.getPageData()
    forecastResult = getForecast.predict_salary(defaultType, workExp)
    return render(request, 'forecastFunction.html', {
        'userInfo': userInfo,
        'types': types,
        'defaultType': defaultType,
        'workExp': workExp,
        'forecastResult': forecastResult,
    })
