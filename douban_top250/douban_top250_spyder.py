#!usr/bin/env python3
# Filename:douban_spyder.py

"""
豆瓣top250电影分析
抓取并保存CSV文件
coding at jun. 2017
"""

import requests
from lxml import html
import re

__author__ = 'JeromeYao'


def douban_top250_spyder():  # 用于抓取的函数主体
    k = 1  # 计数
    for i in range(10):  # 每页25个电影，共10页，程序在其中做循环，抓取信息。
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i * 25)  # 目标网站迭代形式
        text0 = requests.get(url).text  # 请求得到的网页文本内容
        text = html.fromstring(text0)  # 转换为html类数据，便于xpath处理获取信息

        # 所有的信息都在class属性为info的div标签里
        for j in text.xpath('//div[@class="info"]'):
            title = j.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0]  # 影片名称
            info = j.xpath('div[@class="bd"]/p[1]/text()')  # 信息段

            rate = j.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]  # 评分
            com_count0 = j.xpath('div[@class="bd"]/div[@class="star"]/span[4]/text()')[0]  # 评论人数
            com_count = re.match(r'^\d*', com_count0).group()  # 仅保留数字
            quote0 = j.xpath('div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()')  # 短评
            quote = '无' if quote0 == [] else quote0[0].replace(",", "，")  # 若短评不存在则使用‘无’替代

            date = info[1].replace("\n", "").strip(' ').split("\xa0/\xa0")[0]  # 上映日期
            country = info[1].split("\xa0/\xa0")[1]  # 制片国家
            genre = info[1].replace("\n", "").strip(' ').split("\xa0/\xa0")[2]  # 影片类型

            print("TOP%s" % str(k), title, rate, com_count, date, country, genre, quote)  # 打印结果

            # with open("douban_top250_demo.csv", "a") as f:  # 写入文件
                # f.write("%s,%s,%s,%s,%s,%s,%s\n" % (title, rate, com_count, date, country, genre, quote))
            k += 1  # 每条电影信息打印完后计数加一


if __name__ == '__main__':  # 执行代码
    try:
        douban_top250_spyder()
    except:
        print('出现异常')
