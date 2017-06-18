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


def douban_top250_spyder():
    k = 1  # 计数
    for i in range(10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i * 25)
        con = requests.get(url).content
        sel = html.fromstring(con)

        # 所有的信息都在class属性为info的div标签里，可以先把这个节点取出来
        for j in sel.xpath('//div[@class="info"]'):
            title = j.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0]  # 影片名称
            info = j.xpath('div[@class="bd"]/p[1]/text()')  # 信息段

            rate = j.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]  # 评分
            com_count0 = j.xpath('div[@class="bd"]/div[@class="star"]/span[4]/text()')[0]  # 评论人数
            com_count = re.match(r'^\d*', com_count0).group()
            quote0 = j.xpath('div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()')  # 短评
            quote = '无' if quote0 == [] else quote0[0].replace(",", "，")

            date = info[1].replace("\n", "").strip(' ').split("\xa0/\xa0")[0]  # 上映日期
            country = info[1].split("\xa0/\xa0")[1]  # 制片国家
            genre = info[1].replace("\n", "").strip(' ').split("\xa0/\xa0")[2]  # 影片类型

            print("TOP%s" % str(k), title, rate, com_count, date, country, genre, quote)  # 打印结果

            with open("douban_top250.csv", "a") as f:  # 写入文件
                f.write("%s,%s,%s,%s,%s,%s,%s\n" % (title, rate, com_count, date, country, genre, quote))
            k += 1

if __name__ == '__main__':
    douban_top250_spyder()
