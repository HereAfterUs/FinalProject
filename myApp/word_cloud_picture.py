import jieba
from matplotlib import pylab as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from pymysql import connect
import json


def get_img(field, targetImageSrc, resImageSrc):
    con = connect(host="localhost", user='root', password='root', database='infoboss', port=3306, charset='utf8mb4')
    cursor = con.cursor()
    sql = f"select {field} from jobinfo"
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    for i in data:
        if i[0] != '无':
            companyTagsArr = json.loads(i[0])[0].split('，')
            for j in companyTagsArr:
                text += j
    cursor.close()
    con.close()

    # 分词
    data_cut = jieba.cut(text, cut_all=False)
    stop_words = []
    with open('./stopwords', 'r', encoding='utf8') as rf:
        for line in rf:
            if len(line) > 0:
                stop_words.append(line.strip())

    data_result = [x for x in data_cut if x not in stop_words]
    string = ' '.join(data_result)

    wc = WordCloud(
        background_color='white',
        font_path='simkai.ttf',
        scale=10
    )

    wc.generate_from_text(string)

    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')

    plt.savefig(resImageSrc, dpi=500)


get_img('companyTags', '../static/1.png', '../static/companyTags_cloud.jpg')
