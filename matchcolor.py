#!/usr/bin/python
# -*- coding: UTF-8 -*-

from colorsys import hsv_to_rgb
from random import randint
import numpy as np


def color5_generate():
    # HSV,RGB
    color_h = np.array([0., 0., 0., 0., 0.])
    color_s = np.array([0., 0., 0., 0., 0.])
    color_v = np.array([0., 0., 0., 0., 0.])
    color_r = np.array([0., 0., 0., 0., 0.])
    color_g = np.array([0., 0., 0., 0., 0.])
    color_b = np.array([0., 0., 0., 0., 0.])

    mode = randint(0, 12)   # 随机模式
    if mode == 0 or mode == 10:   # 0相同色相 10相近色相
        h = randint(0, 360) / 360.0
        for i in range(0, 5):
            v = randint(5, 95)
            s = randint(10, 95) / 100.0
            color_h[i] = h + randint(-3 * mode, 3 * mode) / 360.0
            color_s[i] = s
            color_v[i] = v / 100.0
    elif mode == 1 or mode == 8:   # 1相同饱和度 8相近饱和度
        s = randint(60, 70)
        for i in range(0, 5):
            h = randint(0, 360) / 360.0
            v = randint(145 - s, 95) / 100.0
            color_h[i] = h
            color_s[i] = s / 100.0 + randint(-2 * mode, 2 * mode) / 100.0
            color_v[i] = v
    elif mode == 2 or mode == 9:   # 2相同亮度 9相近亮度
        v = randint(65, 95)
        for i in range(0, 5):
            h = randint(0, 360) / 360.0
            s = randint(v - 30, 3 * v / 2 - 60) / 100.0
            color_h[i] = h
            color_s[i] = s
            color_v[i] = v / 100.0 + randint(-2 * mode, 3 * mode) / 100.0
    elif mode == 3:   # 黑白
        for i in range(0, 5):
            v = randint(5, 95) / 100.0
            color_h[i] = 0
            color_s[i] = 0
            color_v[i] = v
    elif mode == 4 or mode == 5:   # 4相同色相+相反色相（深色主色） 5（浅色主色）
        h = randint(0, 360) / 360.0
        only = randint(0, 3)   # 选出特别的那个
        for i in range(0, 5):
            if i != only:
                if mode == 4:   # 对比色的亮度范围与原色区分开
                    v = randint(5, 65)
                else:
                    v = randint(70, 95)
                s = randint(95 - v, 95) / 100.0
                color_h[i] = h
                color_s[i] = s
                color_v[i] = v / 100.0
            else:
                if mode == 5:
                    v = randint(5, 65)
                else:
                    v = randint(70, 95)
                s = randint(95 - v, 95) / 100.0
                a = h - 0.5 + randint(-20, 20) / 360.0   # 在一定范围内相反色相
                if a < 0:   # 防止色相小于零
                    a += 1
                color_h[i] = a
                color_s[i] = s
                color_v[i] = v / 100.0
    elif mode == 6 or mode == 7:   # 6黑白+彩色（深色主色） 7（浅色主色）
        h = randint(0, 360) / 360.0
        only = randint(0, 3)
        for i in range(0, 5):
            if i != only:
                if mode == 6:
                    v = randint(5, 45)
                else:
                    v = randint(65, 95)
                color_h[i] = 0
                color_s[i] = 0
                color_v[i] = v / 100.0
            else:
                if mode == 7:
                    v = randint(65, 95)
                else:
                    v = randint(5, 40)
                s = randint(95 - v, 95) / 100.0
                color_h[i] = h
                color_s[i] = s
                color_v[i] = v / 100.0
    elif mode == 11 or mode == 12:   # 11双色（相同色相） 12（相近色相）
        h = randint(0, 360) / 360.0
        only1 = randint(0, 4)   # 选出特别的两个的第一个
        while True:
            only2 = randint(0, 4)   # 选出特别的两个的第二个
            if only2 != only1:   # 不能和第一个是同一个
                break
        for i in range(0, 5):
            if i != only1 and i != only2:
                v = randint(5, 95)
                s = randint(95 - v, 95) / 100.0
                color_h[i] = h + randint(-15 * (mode - 11), 15 * (mode - 11)) / 360.0
                color_s[i] = s
                color_v[i] = v / 100.0
            else:
                v = randint(5, 95)
                s = randint(95 - v, 95) / 100.0
                a = h - 0.5 + randint(-30, 30) / 360.0
                if a < 0:
                    a += 1
                color_h[i] = a
                color_s[i] = s
                color_v[i] = v / 100.0

    for i in range(0, 5):   # 过滤很冲突的颜色的饱和度
        if color_h[i] >= 110 / 360.0 and color_h[i] <= 190 / 360.0 or color_h[i] >= 280 / 360.0 and color_h[i] <= 350 / 360.0:
            if color_s[i] > 0.4 and color_v[i] > 0.7:
                color_s[i] = 0.4 + (color_s[i]-0.4)*0.5
        # 转换RGB
        color_r[i] = (hsv_to_rgb(color_h[i], color_s[i], color_v[i]))[0]
        color_g[i] = (hsv_to_rgb(color_h[i], color_s[i], color_v[i]))[1]
        color_b[i] = (hsv_to_rgb(color_h[i], color_s[i], color_v[i]))[2]
    color5 = np.array([color_r, color_g, color_b])
    '''
             0 1 2 3 4
            R
            G
            B
            color5[(RGB)][01234]
    '''
    return color5
