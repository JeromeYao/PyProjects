# 数据处理

核对数据收集阶段保存的`douban_top250_demo.csv`文件，确认与预期效果一致后，保存为`douban_top250.csv`用于数据处理。
这样可以避免在数据处理阶段反复向豆瓣服务器发出数据请求，被反爬虫机制屏蔽。

数据处理、分析和展示阶段，我们主要任务是格式化数据，根据处理过的数据来制作相应的分析图像。需要导入以下几个`python`库：

```python
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
from collections import Counter
from wordcloud import WordCloud, ImageColorGenerator
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
```

开始处理数据，大致操作思路如下：
先打开文件，再读取整个文件，以逗号分割为列表对象，然后转化为250×7的`ndarray`对象，对应7列数据，每列250个元素，最后将其转换为`DataFrame`对象并加上每列的列名，以方便后续调用。


```python
with open('douban_top250.csv') as f:  # 打开文件
    text_f = f.read().strip()  # 读取文件得到str型文本
list_f = re.split('[,\n]', text_f)  # 分割str文本并转换为list型
array_f = np.array(list_f).reshape(250, 7)  # 转换为250×7的数组
columns_df_f = ['电影名称', '评分', '评分人数', '上映年份', '国家', '类型', '短评']  # 列名
df_f = pd.DataFrame(array_f, columns=columns_df_f)  # 转为DataFrame类
print(df_f)
```

打印得到如下结果：

> ```
  电影名称   评分    评分人数  上映年份   国家    类型  \
0 肖申克的救赎  9.6  833069  1994    美国       犯罪 剧情   
1 这个杀手不太冷  9.4  799185  1994 法国      剧情 动作 犯罪   
2 霸王别姬  9.5  595660  1993   中国大陆 香港   剧情 爱情 同性   
3 阿甘正传  9.4  684515  1994  美国   剧情 爱情   
4 美丽人生  9.5  397936  1997  意大利 剧情 喜剧 爱情 战争   
...      ...      ...   ...    ...   ...    ...
247 彗星来的那一夜  8.3  148590  2013   美国 英国 科幻 悬疑 惊悚   
248 黑鹰坠落  8.5  100794  2001  美国    动作 历史 战争   
249 假如爱有天意  8.2  215610  2003  韩国      剧情 爱情   
               短评  
0             希望让人自由。  
1         怪蜀黍和小萝莉不得不说的故事。  
...              ...
248       还原真实而残酷的战争。  
249          琼瑶阿姨在韩国的深刻版。  
[250 rows x 7 columns]
```

### 片名汇总

`DataFrame`类型的数据在提取列信息方面十分方便。 
汇总榜单上所有电影的名字只需将`df_f`对象的`'电影名称'`元素赋给变量即可。

```python
titles = df_f['电影名称']  # 提取片名列  
print(titles)
```

打印结果如下：

> ```
0         肖申克的救赎
1        这个杀手不太冷
2           霸王别姬
3           阿甘正传
4           美丽人生
5           千与千寻
     ...
244         廊桥遗梦
245         罪恶之城
246         两小无猜
247      彗星来的那一夜
248         黑鹰坠落
249       假如爱有天意
Name: 电影名称, Length: 250, dtype: object
```

### 制片国家及影片类型信息处理
 
处理国家名及影片类型信息的方法与处理片名的方法大同小异。

```python
countries = df_f['国家']  # 提取数组中的国家名数据  
print(countries)
```

这里需要注意观察返回的结果中的：

> ```
2         中国大陆 香港
```

可以看出存在一部影片有多个制作公司的情况，如果要计数则需要解压元素。

```python
list_countries = ' '.join(countries).split()  # 由于存在一部电影有多个制片国家，需要解压出。
print(list_countries)
```
得到列表类的结果如下：  
> ['美国', '法国', '中国大陆', '香港', '美国', '意大利', ... ,'美国', '英国', '美国', '韩国']
  
对列表元素进行计数,使用内置的`collections`库的`Counter`将列表转化为字典，其中`key`为原列表中的元素，`value`为该元素在列表中出现的次数。    
```python
dict_countries0 = Counter(list_countries)  # 转换成字典类并计数
print(dict_countries0)
```
> Counter({'美国': 143, '英国': 34, '日本': 29, '法国': 27,...,'博茨瓦纳': 1, '爱尔兰': 1})

这样也可以很容易得到总共有多少个不同国家出现：
```python
total_countries = len(dict_countries0)  # 字典长度，即出现的不同国家个数
print(total_countries)
```
> 31

```python
num_countries_show = 12  # 控制参数，显示国家的个数，其余用“其他”来概括
dict_countries = list(dict_countries0.most_common(num_countries_show))  # 提取前12个
countries_rest = dict_countries0.most_common()[num_countries_show:]  # 第12个以后合并为一项
size = [i[1] for i in dict_countries]  #
size.append(sum(i[1] for i in countries_rest))
labels = [i[0] for i in dict_countries]
labels.append('其他')
```

榜单上影片的类型的数据处理与制片国家数据处理类似。  

```python
genres = df_f['类型']
list_genres = ' '.join(genres).split()
dict_genres0 = Counter(list_genres)
total_genres = len(dict_genres0)
num_genres_show = 14  # 控制参数，显示类型的个数，其余用“其他”来概括
dict_genres = list(dict_genres0.most_common(num_genres_show))
genres_rest = dict_genres0.most_common()[num_genres_show:]
size = [i[1] for i in dict_genres]
size.append(sum(i[1] for i in genres_rest))
labels = [i[0] for i in dict_genres]
labels.append('其他')
```


### 上榜年份信息处理  

在年份分析部分除了我们需要注意上榜年份为零的数据是不显示的，需要我们另外添加。  

```python
date_movie = df_f['上映年份']
min_date = int(min(date_movie))
max_date = int(max(date_movie))
range_date = range(min_date, max_date + 1)  # 上榜电影年份范围
dict_date0 = Counter(date_movie)  # 转换为年份与对应出现次数的字典
k = [int(key) for key in dict_date0.keys()]  # 构造上榜年份列表
list_date0 = {key: dict_date0[str(key)] if key in k else 0 for key in range_date}  # 以零填充没有上榜的年份的值
dict_date = Counter(list_date0)  # 转换为字典并计数
keys_date, values_date = list(list_date.keys()), list(list_date.values())
```

### 评分、评论人数处理

抓取得到的评分、评论人数的数据可直接调用，处理方法相对比较简单：  

```python
rate_movie = df_f['评分']
index_rate = rate_movie.index + 1  # 序号即排名（从1开始）
values_rate = rate_movie.values  # 得到评分值列表

comments_count = df_f['评分人数']
values_comments = comments_count.values
```