#!usr/bin/env python3
# Filename:wechat_sig_pic.py

"""
For test
"""

import itchat
import re
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import os
import numpy as np
import PIL.Image as Image

# 微信登录
itchat.login()
friends = itchat.get_friends(update=True)[0:]
tList = []
for i in friends:
    signature = i["Signature"].replace(" ", "").replace("span", "").replace("class", "").replace("emoji", "")
    rep = re.compile("1f\d.+")
    signature = rep.sub("", signature)
    tList.append(signature)

# 拼接字符串
text = "".join(tList)

# jieba分词
wordlist_jieba = jieba.cut(text, cut_all=True)
wl_space_split = " ".join(wordlist_jieba)
print(wl_space_split)


# 词云
d = os.path.dirname(__file__)

alice_coloring = np.array(Image.open(os.path.join(d, "xiaohuangren.jpg")))

image_colors = ImageColorGenerator(alice_coloring)

my_wordcloud = WordCloud(background_color="white", max_words=2000, mask=alice_coloring,
                         max_font_size=40, random_state=42).generate(wl_space_split)

plt.imshow(my_wordcloud.recolor(color_func=image_colors))

plt.axis("off")
plt.savefig('exercice_2.png', dpi=500)
plt.show()
