#!usr/bin/env python3
# Filename: douban_top250_analysis.py

"""
豆瓣top250电影分析
数据分析及展示脚本
coding at jun. 2017
"""

import numpy as np
import re
from collections import Counter
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd

__author__ = 'JeromeYao'

with open('douban_top250.csv') as f:  # 打开文件
    text_f = f.read().strip()  # 读取文件得到str型文本

'''
若使用语句 array_f = np.loadtxt('douban_top250.csv', delimiter='d', dtype='str')
打开文档并保存为ndarray类时，会出现报错如下：
UnicodeEncodeError: 'latin-1' codec can't encode characters in position 0-5: ordinal not in range(256)
暂时无法解决。
'''

list_f = re.split('[,\n]', text_f)  # 分割str文本并转换为list型

array_f = np.array(list_f).reshape(250, 7)  # 转换为250×7的数组
df_f = pd.DataFrame(array_f)  # 转为DataFrame类
df_f.columns = ['电影名称', '评分', '评分人数', '上映年份', '国家', '类型', '短评']  # 加上列名
print(df_f)
'''
# 片名汇总
titles = df_f['电影名称']  # 提取片名列
# print(titles)

# 片名词云
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

plt.axis("off")  # 不显示x, y轴下标

plt.savefig('filmCloud_demo.png', dpi=500)  # 保存图片

plt.show()  # 展示图片


# 国家分析
countries = df_f['国家']  # 提取数组中的国家名数据
# print(countries)
list_countries = []  # 初始化国家名列表
for i in countries:  # 由于存在一部电影有多个制片国家，需要解压出。
    for k in i.split():
        list_countries.append(k)
# print(list_countries)
dict_countries = Counter(list_countries)  # 转换成字典类并计数
print(dict_countries)
total_countries = len(dict_countries)  # 字典长度，即出现的不同国家个数
# print(total_countries)

# 类型分析（与国家分析类似）
genres = df_f['类型']

list_genres = []

for i in genres:
    for k in i.split():
        list_genres.append(k)

dict_genres = Counter(list_genres)

total_genres = len(dict_genres)
'''
