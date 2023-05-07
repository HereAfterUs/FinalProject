from .getPublicData import *
import re
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def getPageData():
    return typeList


# 数据读取
df = pd.read_excel("D:\FinalProject\myApp\jobinfo.xlsx", index_col=0)

df['salary'] = df['salary'].apply(lambda x: np.mean([int(i) for i in re.findall('\d+', x)]))
df['workExperience'] = df['workExperience'].replace('在校/应届', '0')
df['workExperience'] = df['workExperience'].apply(lambda x: np.mean([int(i) for i in re.findall('\d+', x)]))


type_enc = OneHotEncoder()
type_encoded = type_enc.fit_transform(df[['type']])
X = pd.DataFrame(type_encoded.toarray())
X['workExperience'] = list(df['workExperience'])

# 训练模型
model = LinearRegression()
model.fit(np.array(X), np.array(df['salary']))

y_pred = model.predict(X)



# plt.scatter(df['workExperience'], df['salary'], color='blue')
# plt.plot(df['workExperience'], y_pred, color='red', linewidth=2)
# plt.title('Salary vs. Work Experience')
# plt.xlabel('Work Experience')
# plt.ylabel('Salary')
# plt.show()


# 定义函数，根据输入的类型和工作经验返回预测的薪资
def predict_salary(types, work_experience):
    if work_experience != '':
        work_experience = int(work_experience)
        if work_experience < 0:
            return None
        mid = pd.DataFrame([types])
        mid.columns = ['type']
        type_encoded = type_enc.transform(mid)
        X = pd.DataFrame(type_encoded.toarray())
        X['workExperience'] = work_experience
        return round(model.predict(np.array(X))[0],2)

    # if work_experience != '':
    #     mid = pd.DataFrame([types])
    #     mid.columns = ['type']
    #     type_encoded = type_enc.transform(mid)
    #     X = pd.DataFrame(type_encoded.toarray())
    #     X['workExperience'] = work_experience
    #     return model.predict(np.array(X))[0]

