#!usr/bin/env python3
# Filename:wechat_gender_analysis.py

"""
分析微信好友男女比例
用plt的饼图展现出来
"""

import itchat
import matplotlib.pyplot as plt

itchat.auto_login(hotReload=True)  # 登录

friends = itchat.get_friends(update=True)[0:]  # 获取好有列表

male = female = other = 0  # 初始化男女计数器

for i in friends[1:]:
    sex = i['Sex']
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other += 1

total = len(friends[1:])

male_percent = float(male) / total * 100
female_percent = float(female) / total * 100
other_percent = float(other) / total * 100

print("男性好友：%.2f%%" % male_percent)
print("女性好友：%.2f%%" % female_percent)
print("其他：%.2f%%" % other_percent)

labels = ('Male', 'Female', 'Others')
size = (male_percent, female_percent, other_percent)

plt.pie(size, labels=labels, autopct='%1.2f%%',
        startangle=90)
plt.axis('equal')
plt.show()

'''
2017.06.08
男性好友：55.80%
女性好友：39.78%
其他：4.42%
'''
