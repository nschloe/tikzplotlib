# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 22:02:04 2022

@author: Niclas
"""

from src.tikzplotlib import save
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111)


x = np.array([7.14, 7.36, 7.47, 7.52, 8.3])
y = np.array([3.3, 4.4, 8.8, 5.5, 9.3])
# ystd = [0.1, 0.5, 0.8, 0.3]
ystd = np.array([(0.1,0.2), (0.5,0.1), (0.8,0.3), (0.3, 0.5), (0.3, 0.5)]).transpose()
xstd = np.array([(np.nan,np.nan), (0.5,0.1), (0.8,0.3), (0.3, 0.5), (0.3, 0.5)]).transpose()
lolims = [True, None, None, True, None]
xlolims = [False, None, None, None, None]
xuplims = [False, None, None, None, None]

eb1 = ax.errorbar(x, y, xerr=0.1, yerr=ystd, ecolor='black', label='1', fmt='d')
eb2 = ax.errorbar(x+1, y+1, xerr=xstd, yerr=ystd, capsize=3, lolims=lolims, xlolims=xlolims, xuplims=xuplims, label='2')
eb3 = ax.errorbar(x+2, y+2, xerr=xstd, yerr=ystd, capsize=3, label='3')
eb4 = ax.errorbar(x+3, y+3, yerr=ystd, capsize=3, label='4')

b6 = ax.bar(x+5,y+5,yerr=ystd, ecolor='green', color= 'red', capsize = 5, label='6')
plt.legend()

save('testBars.tex',standalone=True, encoding='utf8')
