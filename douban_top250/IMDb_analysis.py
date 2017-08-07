#!usr/bin/env python3
# Filename: douban_top250_analysis.py

"""

"""
import requests
from lxml import html
import pandas as pd
import numpy as np

__author__ = 'JeromeYao'

# gather

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Referer': 'http://www.imdb.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/58.0.3029.110 Safari/537.36'
}


def get_html_text(url_x):
    try:
        r = requests.get(url=url_x, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text  # 响应内容
    except:
        return 'Gather Error'


def process_text(text_x):
    text0 = html.fromstring(text_x)
    title_column = '//tbody[@class="lister-list"]/tr/td[@class="titleColumn"]'
    title = text0.xpath(title_column+'/a/text()')
    url_movie0 = text0.xpath(title_column+'/a/@href')
    url_imdb = 'http://www.imdb.com'
    url_movie = [url_imdb+i.split('?')[0] for i in url_movie0]
    date0 = text0.xpath(title_column+'/span/text()')
    date = [i.strip('()') for i in date0]
    rate = text0.xpath('//td[@class="ratingColumn imdbRating"]/strong/text()')
    print('%s\n%s\n%s\n%s' % (title, date, rate, url_movie))
    with open('imdb_top250_demo.csv', 'a') as f:
        f.write('%s\n%s\n%s\n%s' % (title, date, rate, url_movie))
    return '%s\n%s\n%s\n%s' % (title, date, rate, url_movie)

if __name__ == '__main__':
    url = 'http://www.imdb.com/chart/top'
    text = get_html_text(url)
    text1 = process_text(text)



def read_data(path):
    with open(path, 'r') as f:
        text0 = f.readline()
        return text0
path_imdb = 'imdb_top250.csv'

text1 = read_data(path_imdb).replace('"', "'").strip("[]\n'").split("', '")
print(type(read_data(path_imdb)))
title_dict = {'title': text1}
title_df = pd.DataFrame(title_dict)
print(title_df)
