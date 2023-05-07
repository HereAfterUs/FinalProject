from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
import time
import json
import pandas as pd
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinalProject.settings')
django.setup()
from myApp.models import *


class spider(object):
    # 初始化属性
    def __init__(self, type, page):
        self.type = type  # 岗位
        self.page = page  # 页数
        self.spiderUrl = "https://www.zhipin.com/web/geek/job?query=%s&city=100010000&page=%s"  # 目标路径

    def startBrowser(self):
        options = webdriver.ChromeOptions()
        # options.add_experimental_option('debuggerAddress', 'localhost:9222')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        browser = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
        return browser

    def main(self, page):
        if self.page > page:
            return
        browser = self.startBrowser()
        print("正在爬取的页面路径：" + self.spiderUrl % (self.type, self.page))
        browser.get(self.spiderUrl % (self.type, self.page))
        time.sleep(20)
        job_list = browser.find_elements(by=By.XPATH, value="//ul[@class='job-list-box']/li")  # 获取30个li
        for index, job in enumerate(job_list):
            try:
                jobData = []
                print("爬取的是第 %d 条" % (index + 1))
                title = job.find_element(by=By.XPATH, value=".//a[@class='job-card-left']/div[contains(@class,'job-title')]/span[@class='job-name']").text
                addresses = job.find_element(by=By.XPATH, value=".//a[@class='job-card-left']/div[contains(@class,'job-title')]/span[@class='job-area-wrapper']/span").text.split('·')
                address = addresses[0]
                
                if len(addresses) != 1:
                    dist = addresses[1]
                else:
                    dist = ''

                type = self.type

                tag_list = job.find_elements(by=By.XPATH, value=".//a[@class='job-card-left']/div[contains(@class,'job-info')]/ul[@class='tag-list']/li")
                # 是否实习
                if len(tag_list) == 2:
                    # 学历
                    educational = tag_list[1].text
                    # 工作经验
                    workExperience = tag_list[0].text
                else:
                    educational = tag_list[2].text
                    workExperience = tag_list[1].text

                hrName = job.find_element(by=By.XPATH, value=".//a[@class='job-card-left']/div[contains(@class,'job-info')]/div[@class='info-public']").text
                hrWork = job.find_element(by=By.XPATH, value=".//a[@class='job-card-left']/div[contains(@class,'job-info')]/div[@class='info-public']/em").text
                workTag = job.find_elements(by=By.XPATH, value='./div[contains(@class,"job-card-footer")]/ul[@class="tag-list"]/li')
                workTag = json.dumps(list(map(lambda x: x.text, workTag)))  # 数组形式
                practice = 0
                salaries = job.find_element(by=By.XPATH, value=".//a[@class='job-card-left']/div[contains(@class,'job-info')]/span[@class='salary']").text

                if salaries.find('K') != -1:
                    salaries = salaries.split('·')
                    if len(salaries) == 1:
                        salary = list(map(lambda x: int(x) * 1000, salaries[0].replace('K', '').split('-')))
                        salaryMonth = '0薪'
                    else:
                        salary = list(map(lambda x: int(x) * 1000, salaries[0].replace('K', '').split('-')))
                        salaryMonth = salaries[1]
                else:
                    salary = list(map(lambda x: int(x), salaries.replace('元/天', '').split('-')))
                    salaryMonth = '0薪'
                    practice = 1

                companyTitle = job.find_element(by=By.XPATH, value=".//div[@class='job-card-right']/div[@class='company-info']/h3/a").text
                companyAvatar = job.find_element(by=By.XPATH, value=".//div[@class='job-card-right']/div[@class='company-logo']/a/img").get_attribute("src")

                #  ----------------------------------------------------------------
                companyInfos = job.find_elements(by=By.XPATH, value=".//div[@class='job-card-right']/div[@class='company-info']/ul[@class='company-tag-list']/li")
                if len(companyInfos) == 3:  # 说明存在融资标签
                    companyNature = companyInfos[0].text
                    companyStatus = companyInfos[1].text
                    companyPeoples = companyInfos[2].text

                    if companyPeoples != '10000人以上':
                        companyPeople = list(map(lambda x: int(x), companyInfos[2].text.replace('人', '').split('-')))
                    else:
                        companyPeople = [0, 10000]
                else:  # 说明融资标签有问题
                    companyNature = companyInfos[0].text
                    companyStatus = '未融资'
                    companyPeoples = companyInfos[1].text

                    if companyPeoples != '10000人以上':
                        companyPeople = list(map(lambda x: int(x), companyInfos[1].text.replace('人', '').split('-')))
                    else:
                        companyPeople = [0, 10000]
                #  ----------------------------------------------------------------

                companyTags = job.find_element(by=By.XPATH, value='./div[contains(@class,"job-card-footer")]/div[@class="info-desc"]').text
                if not companyTags:
                    companyTags = '无'
                else:
                    companyTags = json.dumps(companyTags.split(','))

                # 详情地址
                detailUrl = job.find_element(by=By.XPATH, value=".//a[@class='job-card-left']").get_attribute('href')
                # 公司详情
                companyUrl = job.find_element(by=By.XPATH, value=".//div[@class='job-card-right']/div[@class='company-info']/h3/a").get_attribute('href')

                # print(title, address, type, educational, workExperience, workTag, salary, salaryMonth,
                #          companyTags, hrWork, hrName, practice, companyTitle, companyAvatar, companyNature,
                #          companyStatus, companyPeople, detailUrl, companyUrl, dist)

                jobData.append(title)
                jobData.append(address)
                jobData.append(type)
                jobData.append(educational)
                jobData.append(workExperience)
                jobData.append(workTag)
                jobData.append(salary)
                jobData.append(salaryMonth)
                jobData.append(companyTags)
                jobData.append(hrWork)
                jobData.append(hrName)
                jobData.append(practice)
                jobData.append(companyTitle)
                jobData.append(companyAvatar)
                jobData.append(companyNature)
                jobData.append(companyStatus)
                jobData.append(companyPeople)
                jobData.append(detailUrl)
                jobData.append(companyUrl)
                jobData.append(dist)

                self.save_to_csv(jobData)
            except:
                pass

        self.page += 1
        self.main(page)

    def clear_csv(self):
        df = pd.read_csv('./temp.csv')
        df.dropna(inplace=True)  # 清除缺失值
        df.drop_duplicates(inplace=True)
        df['salaryMonth'] = df['salaryMonth'].map(lambda x: x.replace('薪', ''))
        print("总条数为%d" % df.shape[0])
        return df.values

    def save_to_sql(self):
        data = self.clear_csv()
        for job in data:
            JobInfo.objects.create(
                title=job[0],
                address=job[1],
                type=job[2],
                educational=job[3],
                workExperience=job[4],
                workTag=job[5],
                salary=job[6],
                salaryMonth=job[7],
                companyTags=job[8],
                hrWork=job[9],
                hrName=job[10],
                practice=job[11],
                companyTitle=job[12],
                companyAvatar=job[13],
                companyNature=job[14],
                companyStatus=job[15],
                companyPeople=job[16],
                detailUrl=job[17],
                companyUrl=job[18],
                dist=job[19]
            )

        print("导入数据库成功")

        os.remove("./temp.csv")

    def save_to_csv(self, rowData):
        with open('./temp.csv', 'a', newline='', encoding='utf-8') as wf:
            writer = csv.writer(wf)
            writer.writerow(rowData)

    def init(self):
        if not os.path.exists('./temp.csv'):
            with open('./temp.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["title", "address", "type", "educational", "workExperience", "workTag", "salary", "salaryMonth",
                     "companyTags", "hrWork", "hrName", "practice", "companyTitle", "companyAvatar", "companyNature",
                     "companyStatus", "companyPeople", "detailUrl", "companyUrl", "dist"])

    # 岗位名字 省份地址 岗位 学历 工作经验 工作标签 薪资 年底多薪
    # 公司福利标签 HR职位 HR名字 判断是否为实习生 公司名称 公司图标 公司性质
    # 公司状态 公司人数 详情页 公司详情页 行政区域


if __name__ == '__main__':
    spiderObj = spider("全栈工程师", 1)
    spiderObj.init()
    spiderObj.main(10)
    spiderObj.save_to_sql()
