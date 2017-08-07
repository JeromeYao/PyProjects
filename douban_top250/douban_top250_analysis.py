#!usr/bin/env python3
# Filename: douban_top250_analysis.py

"""
豆瓣top250电影分析
数据分析及展示脚本

coding at jun. 2017
"""

import re
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
from collections import Counter
from wordcloud import WordCloud, ImageColorGenerator
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

__author__ = 'JeromeYao'


with open('douban_top250.csv') as f:  # 打开文件
    text_f = f.read().strip()  # 读取文件得到str型文本
'''
若使用语句: 
array_f = np.loadtxt('douban_top250.csv', delimiter=',', dtype='str')
打开文档并保存为ndarray类时，会出现报错如下：
UnicodeEncodeError: 'latin-1' codec can't encode characters in position 0-5: ordinal not in range(256)
暂时无法解决。
'''
list_f = re.split('[,\n]', text_f)  # 分割str文本并转换为list型
array_f = np.array(list_f).reshape(250, 7)  # 转换为250×7的数组
columns_df_f = ['电影名称', '评分', '评分人数', '上映年份', '国家', '类型', '短评']  # 列名
df_f = pd.DataFrame(array_f, columns=columns_df_f)  # 转为DataFrame类

# 片名词云

titles = df_f['电影名称']  # 提取片名列

text_titles = r' '.join(titles)  # 列表转换成str类
alice_coloring = np.array(Image.open("film.jpg"))  # 读取mask/color图片
image_colors = ImageColorGenerator(alice_coloring)  # 颜色生成器
my_wordcloud = WordCloud(background_color="white",  # 设置背景颜色
                         max_words=2000,  # 设置最大实现的字数
                         mask=alice_coloring,  # 设置背景照片
                         max_font_size=30,  # 设置字体最大值
                         random_state=1  # 设置随机配色数
                         ).generate(text_titles)  # 根据titles生成词云
plt.imshow(my_wordcloud.recolor(color_func=image_colors))  # 再上色并显示
plt.title(s='Douban Top-250 rated movies analysis', fontsize=20)  # 标题
plt.text(800, 700, 'By: Jerome Yao', fontsize=8)  # 签名
plt.axis("off")  # 不显示x, y轴
plt.savefig('filmCloud_demo.png', dpi=500)  # 保存图片
plt.show()  # 展示图片

# 国家分析

countries = df_f['国家']  # 提取数组中的国家名数据
list_countries = ' '.join(countries).split()  # 由于存在一部电影有多个制片国家，需要解压出。
dict_countries0 = Counter(list_countries)  # 转换成字典类并计数
total_countries = len(dict_countries0)  # 字典长度，即出现的不同国家个数
num_countries_show = 12  # 控制参数，显示国家的个数，其余用“其他”来概括
dict_countries = list(dict_countries0.most_common(num_countries_show))  # 提取前12个
countries_rest = dict_countries0.most_common()[num_countries_show:]  # 第12个以后合并为一项
size = [i[1] for i in dict_countries]  # 前12个‘个数’转化为列表
size.append(sum(i[1] for i in countries_rest))  # 剩余的求和
labels = [i[0] for i in dict_countries]  # 前12个‘国家名’转化为列表
labels.append('其他')  # 剩下的合为“其他”

font_initial = matplotlib.rcParams['font.family']  # 初始字体
matplotlib.rcParams['font.family'] = 'Droid Sans Fallback'  # 修改字体
ax0 = plt.subplot()  # 创建子作图区
ax0.set_title('各制片国上榜次数统计环形图')  # 标题
ax0.pie(size, labels=labels, shadow=False, startangle=90)  # 做饼图
matplotlib.rcParams['font.family'] = font_initial  # 还原字体
ax0.pie(size, labels=size, radius=0.6, startangle=90, labeldistance=1.2)  # 环内文本
ax0.pie([1], radius=0.6, colors='w')  # 白心
ax0.axis('equal')  # 正圆
plt.savefig('countries_demo.png', dpi=300)  # 保存图片
plt.show()

# 类型分析（与国家分析类似）

genres = df_f['类型']
list_genres = ' '.join(genres).split()
dict_genres0 = Counter(list_genres)
total_genres = len(dict_genres0)
num_genres_show = 14
dict_genres = list(dict_genres0.most_common(num_genres_show))
genres_rest = dict_genres0.most_common()[num_genres_show:]
size = [i[1] for i in dict_genres]
size.append(sum(i[1] for i in genres_rest))
labels = [i[0] for i in dict_genres]
labels.append('其他')

font_initial = matplotlib.rcParams['font.family']
matplotlib.rcParams['font.family'] = 'Droid Sans Fallback'
ax1 = plt.subplot()
ax1.set_title('各电影类型上榜次数统计环形图')
ax1.pie(size, labels=labels, shadow=False, startangle=90)
matplotlib.rcParams['font.family'] = font_initial
ax1.pie(size, labels=size, radius=0.6, startangle=90, labeldistance=1.25)
ax1.pie([1], radius=0.6, colors='w')
ax1.axis('equal')
plt.savefig('genres_demo.png', dpi=300)
plt.show()

# 上榜年份

date_movie = df_f['上映年份']  # 提取
min_date = int(min(date_movie))
max_date = int(max(date_movie))
range_date = range(min_date, max_date + 1)  # 上榜电影年份范围
dict_date0 = Counter(date_movie)  # 转换为年份与对应出现次数的字典
k = [int(key) for key in dict_date0.keys()]  # 构造上榜年份列表
list_date0 = {key: dict_date0[str(key)] if key in k else 0 for key in range_date}  # 以零填充没有上榜的年份的值
list_date = Counter(list_date0)  # 转换为字典并计数
keys_date, values_date = list(list_date.keys()), list(list_date.values())

ax2 = plt.subplot()
ax2.set_title('各年份上榜次数', fontproperties='Droid Sans Fallback')  # 标题，单处修改字体
ax2.set_xlabel('年份', fontproperties='Droid Sans Fallback')  # x轴标签
ax2.set_xlim(1930, 2020)
ax2.set_ylabel('上榜次数', fontproperties='Droid Sans Fallback')  # y轴标签
ax2.bar(keys_date, values_date)  # 画柱状图
plt.savefig('date_demo.png', dpi=300)
plt.show()

# 评分

rate_movie = df_f['评分']
index_rate = rate_movie.index + 1  # 序号即排名（从1开始）
values_rate = rate_movie.values  # 得到评分值列表

ax3 = plt.subplot()
ax3.set_title('电影排名与评分的关系', fontproperties='Droid Sans Fallback')
ax3.set_xlabel('排名', fontproperties='Droid Sans Fallback')
ax3.set_ylabel('评分', fontproperties='Droid Sans Fallback')
ax3.plot(index_rate, values_rate, 'blue')  # 画折线图
plt.savefig('rate_movie_demo.png', dpi=300)
plt.show()

x = np.array(index_rate)
y = np.array(values_rate)
degree = [1, 3, 10]
ax3 = plt.subplot()
ax3.set_title('电影排名与评分的关系', fontproperties='Droid Sans Fallback')
ax3.set_xlabel('排名', fontproperties='Droid Sans Fallback')
ax3.set_ylabel('评分', fontproperties='Droid Sans Fallback')
ax3.plot(index_rate, values_rate, 'cyan', linewidth=0.7)  # 原数据图
for d in degree:
    clf = Pipeline([('poly', PolynomialFeatures(degree=d)),  # 产生多项式
                    ('linear', linear_model.Ridge())])  # 岭回归
    clf.fit(x[:, np.newaxis], y)  # 执行计算
    y_test = clf.predict(x[:, np.newaxis])  # 计算得到值
    theta_list = clf.named_steps['linear'].coef_  # 计算多项式系数
    intercept = clf.named_steps['linear'].intercept_  # 计算截距
    r2 = clf.score(x[:, np.newaxis], y)  # 计算R2
    print('Poly Degree:' + str(d), 'Theta List:' + str(theta_list), 'Intercept:' + str(intercept),
          'R^2:' + str(r2), '', sep='\n')  # 打印系数、截距、R2
    plt.plot(x, y_test, linewidth=2)  # 拟合多项式图像
plt.grid()  # 网格
plt.legend(['Data', 'Poly Degree:' + str(degree[0]), 'Poly Degree:' + str(degree[1]), 'Poly Degree:' + str(degree[2])],
           loc='upper right')  # 标注
plt.savefig('rate_movie_regress_demo.png', dpi=300)
plt.show()

# 评论人数

comments_count = df_f['评分人数']
values_comments = comments_count.values

cm = plt.cm.get_cmap('rainbow')
ax4 = plt.subplot()
ax4.set_title('电影评分与评分人数、排名三维关系散点图', fontproperties='Droid Sans Fallback')
ax4.set_xlabel('排名', fontproperties='Droid Sans Fallback')
ax4.set_ylabel('评论人数', fontproperties='Droid Sans Fallback')
sc = ax4.scatter(index_rate, values_comments, c=values_rate, s=8, marker='o', cmap=cm)
plt.colorbar(sc)
plt.savefig('comment_rate_demo.png', dpi=300)
plt.show()
