#!usr/bin/env python3
# Filename:regression.py

"""
Polynomial Regression demo
ubuntu 17.04 python 3.6
jul. 2017
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.stats import norm
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
# from sklearn import linear_model

__author__ = 'JeromeYao'


# 数据生成

x = np.arange(0, 1, 0.002)
y = norm.rvs(0, size=500, scale=0.1)
y = y + x**2


def rmse(y_test0, y):
    """ 均方误差根 """
    return sp.sqrt(sp.mean((y_test0 - y) ** 2))


def r2(y_test0, y_true):
    """ 与均值相比的优秀程度，介于[0~1]。0表示不如均值。1表示完美预测.这个版本的实现是参考sklearn官网文档  """
    return 1 - ((y_test0 - y_true)**2).sum() / ((y_true - y_true.mean())**2).sum()


def r22(y_test0, y_true):
    """这是Conway&White《机器学习使用案例解析》里的版本"""
    y_mean = np.array(y_true)
    y_mean[:] = y_mean.mean()
    return 1 - rmse(y_test0, y_true) / rmse(y_mean, y_true)


plt.scatter(x, y, s=5)
degree = [1, 2, 100]
y_test = []
y_test = np.array(y_test)


for d in degree:
    clf = Pipeline([('poly', PolynomialFeatures(degree=d)),
                   ('linear', LinearRegression(fit_intercept=False))])
    clf.fit(x[:, np.newaxis], y)
    y_test = clf.predict(x[:, np.newaxis])
    print(clf.named_steps['linear'].coef_)
    print('rmse=%.2f, R2=%.2f, r22=%.2f, clf.score=%.2f' % (rmse(y_test, y), r2(y_test, y),
                                                            r22(y_test, y), clf.score(x[:, np.newaxis], y)))
    plt.plot(x, y_test, linewidth=2)

plt.grid()
plt.legend(['1', '2', '100'], loc='upper left')
plt.show()
