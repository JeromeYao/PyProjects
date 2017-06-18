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

__author__ = 'JeromeYao'

with open('douban_top250.csv') as f:  # 打开文件
    text_f = f.read().strip()  # 读取文件得到str型文本

list_f = re.split('[,\n]', text_f)  # 分割str文本并转换为list型

array_f = np.array(list_f).reshape(250, 7)  # 转换为250×5的数组

'''
# 片名汇总
titles = array_f[:, 0]  # 提取片名列

# 片名词云
text_titles = r' '.join(titles)  # 列表转换成str类

alice_coloring = np.array(Image.open("film.jpg"))  # 读取mask/color图片

image_colors = ImageColorGenerator(alice_coloring)  #

my_wordcloud = WordCloud(background_color="white",  # 设置背景颜色
                         max_words=2000,  # 设置最大实现的字数
                         mask=alice_coloring,  # 设置背景照片
                         max_font_size=30,  # 设置字体最大值
                         random_state=1  # 设置随机配色数
                         ).generate(text_titles)  # 根据titles生成词云

plt.imshow(my_wordcloud.recolor(color_func=image_colors))  # 再上色并显示

plt.axis("off")  # 不显示轴下标

plt.savefig('filmCloud_test.png', dpi=500)  # 保存图片

plt.show()  # 展示图片
'''

# 国家分析
countries = array_f[:, 4]  # 提取数组中的国家名数据

list_countries = []  # 初始化国家名列表

for i in countries:
    for k in i.split():
        list_countries.append(k)
# print(list_countries)
dict_countries = Counter(list_countries)
# print(dict_countries)
total_countries = len(dict_countries)
# print(total_countries)

# 类型分析
genres = array_f[:, 5]

list_genres = []

for i in genres:
    for k in i.split():
        list_genres.append(k)
# print(list_genres)
dict_genres = Counter(list_genres)
# print(dict_genres)
total_genres = len(dict_genres)
# print(total_countries)
