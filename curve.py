# -*- coding: utf-8 -*-

import numpy as np
from scipy import interpolate
# import matplotlib.pyplot as plt
from random import randint
from math import sqrt,pow,sin,pi

def curve_path_generate(ori_pos,ter_pos,rand_border_l,rand_border_r,rand_border_t,rand_border_b):
    t = np.array([num for num in range(4)])
    y = np.array([ori_pos[0], 0, 0, ter_pos[0]])
    x = np.array([ori_pos[1], 0, 0, ter_pos[1]])
    while True:
        x[1] = randint(rand_border_l, rand_border_r)
        y[1] = randint(rand_border_t, rand_border_b)
        if pow((x[1] - x[0]), 2) + pow((y[1] - y[0]), 2) > 22500 and pow((x[1] - x[3]), 2) + pow((y[1] - y[3]), 2) > 22500:
            break
    while True:
        x[2] = randint(rand_border_l, rand_border_r)
        y[2] = randint(rand_border_t, rand_border_b)
        if pow((x[2] - x[0]), 2) + pow((y[2] - y[0]), 2) > 22500 and pow((x[2] - x[1]), 2) + pow((y[2] - y[1]), 2) > 22500 and pow((x[2] - x[3]), 2) + pow((y[2] - y[3]), 2) > 22500:
            break
    dotx = np.array([0.0 for i in range(50)])
    doty = np.array([0.0 for i in range(50)])
    # 插值法之后的t轴值，表示从0到3间距为0.0001的30000个数
    tnew = np.arange(0, 3.0001, 0.0001)
    """    kind方法：nearest、zero、slinear、quadratic、cubic    实现函数func()    """
    func = interpolate.interp1d(t, x, kind='cubic')
    # 利用xnew和func函数生成ynew，xnew的数量等于ynew数量
    xnew = func(tnew)
    func = interpolate.interp1d(t, y, kind='cubic')
    ynew = func(tnew)
    lf = length = 0
    for i in range(len(tnew) - 1):
        length += sqrt(pow((xnew[i + 1] - xnew[i]), 2) + pow((ynew[i + 1] - ynew[i]), 2))
    dotx[0] = xnew[0]
    doty[0] = ynew[0]
    dotx[49] = xnew[len(tnew) - 1]
    doty[49] = ynew[len(tnew) - 1]
    a = 1
    lb = sqrt(pow((xnew[0] - xnew[1]), 2) + pow((ynew[0] - ynew[1]), 2))
    # print length
    for i in range(0, len(tnew) - 2):
        lf += sqrt(pow((xnew[i + 1] - xnew[i]), 2) + pow((ynew[i + 1] - ynew[i]), 2))
        lb += sqrt(pow((xnew[i + 1] - xnew[i + 2]), 2) + pow((ynew[i + 1] - ynew[i + 2]), 2))
        q_len = 1+1*sin(a*pi/100) * length
        # print 'a =', a, abs(a * length / 30.0), '-', l, '=', abs(a * length / 30.0 - l)
        if q_len >= lf and q_len <= lb:
            if q_len - lf <= lb - q_len:
                dotx[a] = xnew[i]
                doty[a] = ynew[i]
            else:
                dotx[a] = xnew[i+1]
                doty[a] = ynew[i+1]
            a += 1
        if a > 48:
            break

    point = np.array([dotx, doty])

    # 画图部分

    '''plt.plot(xnew, ynew)
    #plt.plot(x, y, 'ro')
    plt.plot(dotx, doty, 'x-')
    plt.show()'''
    return point

# print curve_path_generate([0,0],[100,100],0,100,0,100)
