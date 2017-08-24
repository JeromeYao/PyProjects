#!usr/bin/env python3
# Filename:possion_test.py
"""
我们来思考一下，每年上榜的电影数都是可数集，样本空间为 ![](/assets/latex001.gif)。
取一个极大自然数`n`,我们可以把一个年份分解为等长的`n`段，即![](/assets/latex002.gif)
当`n`很大时，每个小区间段有两部电影上榜的概率可以忽略不计。假设每段时间电影上榜的概率相等，即每部电影上榜的概率是独立的，
且反比于`n`，不妨假设为 ![](/assets/latex003.gif),那么一年内总的上榜电影数为：

![](/assets/latex004.gif)
当![](/assets/latex005.gif) 取极限时,有:
![](/assets/latex006.gif)

我们来总结一下该问题，其满足以下三个特点：

1. 从宏观角度上来看电影上榜TOP250是小概率事件；
2. 电影之间是独立的，也即不会互相依赖或者影响；
3. 电影上榜的概率是稳定的，即必然有250部电影会上榜。

在统计学上，如果某类事件满足上述三个条件，就称它服从泊松分布，所以我们考虑以泊松分布拟合该图像，泊松分布的概率函数为：
![](/assets/latex007.gif)
在这函数中有个重要参数：![](/assets/latex008.gif)， 它代表单位时间内随机事件的平均发生率。

~~拟合图像暂略~~
"""
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import pandas as pd
import re
from collections import Counter

__author__ = 'JeromeYao'

with open('douban_top250.csv') as f:  # 打开文件
    text_f = f.read().strip()  # 读取文件得到str型文本
list_f = re.split('[,\n]', text_f)  # 分割str文本并转换为list型
array_f = np.array(list_f).reshape(250, 7)  # 转换为250×7的数组
columns_df_f = ['电影名称', '评分', '评分人数', '上映年份', '国家', '类型', '短评']  # 列名
df_f = pd.DataFrame(array_f, columns=columns_df_f)  # 转为DataFrame类

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
ax2.set_xlim(1930, 2020)  # 横轴上下限
ax2.set_ylabel('上榜次数', fontproperties='Droid Sans Fallback')  # y轴标签
ax2.bar(keys_date, values_date)  # 画柱状图
rv = st.poisson(1999)  # 泊松分布
print(rv)
x = range(len(values_date))
print(x)
# ax2.plot(x, rv, lw=5, c='r')
# plt.savefig('date_demo.png', dpi=300)
plt.show()
