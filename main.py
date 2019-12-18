#!/usr/bin/python
# -*- coding: UTF-8 -*-

from random import randint
from math import cos, pi
from colorsys import rgb_to_hsv
import numpy as np
from curve import curve_path_generate
from matchcolor import color5_generate
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window


def get2_hex(x):
    y = hex(x)
    if y[3] == 'L':
        z = ['0',y[2]]
    else:
        z = [y[2],y[3]]
    return z


class Circle1(Widget):
    rad = 100
    old_pos = [0, 0]
    new_pos = [0, 0]
    old_col = np.array([0, 0, 0])
    new_col = np.array([0, 0, 0])
    micro_color = np.array([0, 0, 0])
  
    
class Circle2(Widget):
    rad = NumericProperty(0)
    old_pos = [0, 0]
    new_pos = [0, 0]
    old_col = np.array([0, 0, 0])
    new_col = np.array([0, 0, 0])
    micro_color = np.array([0, 0, 0])
    
    
class Circle3(Widget):
    rad = NumericProperty(0)
    old_pos = [0, 0]
    new_pos = [0, 0]
    old_col = np.array([0, 0, 0])
    new_col = np.array([0, 0, 0])
    micro_color = np.array([0, 0, 0])


class Circle4(Widget):
    rad = NumericProperty(0)
    old_pos = [0, 0]
    new_pos = [0, 0]
    old_col = np.array([0, 0, 0])
    new_col = np.array([0, 0, 0])
    micro_color = np.array([0, 0, 0])


class Digit(GridLayout):   # 数字字母阵列
    digit_num = [[i for i in range(0, 6)] for j in range(0, 5)]
    col_opa_new = 0   # 用于混合在背景上的透明度
    col_opa_old = 0

    def __init__(self, **kwargs):
        super(Digit, self).__init__(**kwargs)
        self.cols = 5   # 五列数字字母
        for i in range(0, 6):
            for j in range(0, 5):
                self.digit_num[j][i] = Label(text=str(i), font_name='Square', font_size='40', opacity='0')
                self.add_widget(self.digit_num[j][i])


class Background(Widget):
    old_col = np.array([0, 0, 0])
    new_col = np.array([0, 0, 0])
    micro_color = np.array([0, 0, 0])


class Arena(Widget):
    circle1 = ObjectProperty(None)
    circle2 = ObjectProperty(None)
    circle3 = ObjectProperty(None)
    circle4 = ObjectProperty(None)
    background = ObjectProperty(None)
    event_col = 0   # 变色时钟事件
    event_opa_pre = 0   # 字阵淡入时钟事件
    event_opa_post = 0   # 字阵淡出时钟事件
    time_circle = 1   # 圆与背景变化的时间微元
    time_digit = 1   # 数字字母变化的时间微元
    point1 = np.array([[0], [0]])   # 路径点列
    point2 = np.array([[0], [0]])
    point3 = np.array([[0], [0]])
    point4 = np.array([[0], [0]])
    digit = Digit()   # 字阵对象

    def __init__(self, **kwargs):
        super(Arena, self).__init__(**kwargs)
        Window.size = (540, 960)
        self.size = Window.size
        self.digit.size[0] = self.size[0] * 3 / 4
        self.digit.size[1] = self.size[1] * 3 / 5
        self.digit.center = self.center
        self.add_widget(self.digit)

    def wait(self, dt):
        self.new()

    def new(self):
        # 随机新坐标
        Circle4.new_pos = Circle3.new_pos = Circle2.new_pos = Circle1.new_pos = randint(0, self.right - self.circle1.rad), randint(0, self.top - self.circle1.rad)
        Circle4.old_pos = Circle3.old_pos = Circle2.old_pos = Circle1.old_pos = self.circle1.pos  # 记录旧坐标
        # 换色
        color_match = color5_generate()
        Circle1.old_col = self.circle1.col
        Circle1.new_col = np.array([color_match[0][0], color_match[1][0], color_match[2][0]])
        Circle1.micro_color = (Circle1.new_col - Circle1.old_col) / 60.0
        Circle2.old_col = self.circle2.col
        Circle2.new_col = np.array([color_match[0][1], color_match[1][1], color_match[2][1]])
        Circle2.micro_color = (Circle2.new_col - Circle2.old_col) / 60.0
        Circle3.old_col = self.circle3.col
        Circle3.new_col = np.array([color_match[0][2], color_match[1][2], color_match[2][2]])
        Circle3.micro_color = (Circle3.new_col - Circle3.old_col) / 60.0
        Circle4.old_col = self.circle4.col
        Circle4.new_col = np.array([color_match[0][3], color_match[1][3], color_match[2][3]])
        Circle4.micro_color = (Circle4.new_col - Circle4.old_col) / 60.0
        Background.old_col = self.background.col
        Background.new_col = np.array([color_match[0][4], color_match[1][4], color_match[2][4]])
        Background.micro_color = (Background.new_col - Background.old_col) / 60.0
        a = rgb_to_hsv(Background.new_col[0], Background.new_col[1], Background.new_col[2])
        Digit.col_opa_new = a[2] - a[1] / 2.0 + 0.6
        # 计算路径
        self.point1 = curve_path_generate(Circle1.old_pos, Circle1.new_pos, 0, self.top - 1 * self.circle1.rad, 0, self.right - 1 * self.circle1.rad)
        self.point2 = curve_path_generate(Circle2.old_pos, Circle2.new_pos, 0, self.top - 1 * self.circle1.rad, 0, self.right - 1 * self.circle1.rad)
        self.point3 = curve_path_generate(Circle3.old_pos, Circle3.new_pos, 0, self.top - 1 * self.circle1.rad, 0, self.right - 1 * self.circle1.rad)
        self.point4 = curve_path_generate(Circle4.old_pos, Circle4.new_pos, 0, self.top - 1 * self.circle1.rad, 0, self.right - 1 * self.circle1.rad)

    def on_touch_down(self, touch):
        self.circle1.rad = self.circle1.size[1]   # 得到半径
        if self.circle1.collide_point(touch.x, touch.y) and self.event_col == 0:
            # 数字淡入时钟开始
            self.event_opa_pre = Clock.schedule_interval(self.update_opa_pre, 1.0 / 60.0)
            # 移动与变色时钟开始
            self.event_col = Clock.schedule_interval(self.update_col, 1.0 / 60.0)

    def update_opa_pre(self, dt):   # 字阵淡入
        if isinstance(self.event_opa_post, int) == 0:   # 判断淡出是否已停止
            self.event_opa_post.cancel()
            self.event_opa_post = 0
            self.time_digit = (80 - self.time_digit) * 15 / 80   # 校准透明度
        Digit.col_opa_old = self.digit.digit_num[0][0].color[3]   # 获得先前的用于混合在背景上的透明度
        self.time_digit += 1
        for i in range(0, 6):
            for j in range(0, 5):
                self.digit.digit_num[j][i].opacity = 0.25 - 0.25 * cos(self.time_digit * pi / 15.0)   # 淡入主透明度
                # 淡入到新的用于混合在背景上的透明度
                self.digit.digit_num[j][i].color[3] = self.time_digit * (self.digit.col_opa_new - self.digit.col_opa_old) / 15
        if self.time_digit > 15:   # 超出时间停止时钟
            self.time_digit = 1   # 复位时间微元
            self.event_opa_pre.cancel()

    def update_opa_post(self, dt):   # 字阵淡出
        self.time_digit += 1
        for i in range(0, 6):
            for j in range(0, 5):
                self.digit.digit_num[j][i].opacity = 0.25 + 0.25 * cos(self.time_digit * pi / 80.0)   # 淡出主透明度
        if self.time_digit > 80:   # 超出时间停止时钟
            self.time_digit = 1   # 复位时间微元
            self.event_opa_post.cancel()
            self.event_opa_post = 0   # 定义为整数表示已时钟停止

    def update_col(self, dt):   # 移动与变色
        self.move(self.time_circle)
        self.time_circle += 1
        if self.time_circle > 50:   # 超出时间停止时钟
            self.time_circle = 1   # 复位时间微元
            self.event_opa_post = Clock.schedule_interval(self.update_opa_post, 1.0 / 60.0)
            self.event_col.cancel()
            self.event_col = 0
            Clock.schedule_once(self.wait)   # 防止卡在最后一帧并计算下一轮位置和颜色

    def move(self, time_circle):
        self.circle1.x = int(self.point1[1][time_circle - 1])
        self.circle1.y = int(self.point1[0][time_circle - 1])
        self.circle2.x = int(self.point2[1][time_circle - 1] + 20)
        self.circle2.y = int(self.point2[0][time_circle - 1] + 20)
        self.circle3.x = int(self.point3[1][time_circle - 1] + 40)
        self.circle3.y = int(self.point3[0][time_circle - 1] + 40)
        self.circle4.x = int(self.point4[1][time_circle - 1] + 60)
        self.circle4.y = int(self.point4[0][time_circle - 1] + 60)
        self.circle1.col = self.circle1.col + Circle1.micro_color
        self.circle2.col = self.circle2.col + Circle2.micro_color
        self.circle3.col = self.circle3.col + Circle3.micro_color
        self.circle4.col = self.circle4.col + Circle4.micro_color
        self.background.col = self.background.col + Background.micro_color
        for i in range(0, 3):
            self.digit.digit_num[0][2 * i].text = get2_hex(self.circle1.col[i] * 255)[0]
            self.digit.digit_num[0][2 * i + 1].text = get2_hex(self.circle1.col[i] * 255)[1]
            self.digit.digit_num[1][2 * i].text = get2_hex(self.circle2.col[i] * 255)[0]
            self.digit.digit_num[1][2 * i + 1].text = get2_hex(self.circle2.col[i] * 255)[1]
            self.digit.digit_num[2][2 * i].text = get2_hex(self.circle3.col[i] * 255)[0]
            self.digit.digit_num[2][2 * i + 1].text = get2_hex(self.circle3.col[i] * 255)[1]
            self.digit.digit_num[3][2 * i].text = get2_hex(self.circle4.col[i] * 255)[0]
            self.digit.digit_num[3][2 * i + 1].text = get2_hex(self.circle4.col[i] * 255)[1]
            self.digit.digit_num[4][2 * i].text = get2_hex(self.background.col[i] * 255)[0]
            self.digit.digit_num[4][2 * i + 1].text = get2_hex(self.background.col[i] * 255)[1]
        # 单次移动


class CircleEscapeApp(App):
    def build(self):
        arena = Arena()
        arena.new()   # 提前计算新的路径
        return arena


if __name__ == '__main__':
    CircleEscapeApp().run()
