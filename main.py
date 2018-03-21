# !/usr/bin/env python
# coding:utf-8
__author__ = 'oupei'
import os
import numpy
import PIL
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

need_update = True

# 获取手机屏幕截图并发送到电脑上
def get_screen_image():
    os.system('adb shell screencap -p /sdcard/screen.png')
    os.system('adb pull /sdcard/screen.png')
    return numpy.array(PIL.Image.open('screen.png'))

# 根据用户点击鼠标的位置计算跳的距离从而计算出按屏幕的时间
def jump_to_next(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    dis = ((x1-x2)**2 + (y1-y2)**2)**0.5	# 计算距离
	# 计算按屏幕时间
    os.system('adb shell input swipe 320 410 320 410 {}'.format(int(dis*1.35)))
    global need_update
    need_update = True

# 定义鼠标点击函数
def on_click(event, coor=[]):
    coor.append((event.xdata, event.ydata))
    if len(coor) == 2:
        jump_to_next(coor.pop(), coor.pop())

# 更新下一张图片		
def update_screen(frame):
    global need_update
    if need_update:
        time.sleep(0.5)
        axes_image.set_array(get_screen_image())
        need_update = False
    return axes_image,

figure = plt.figure()
# 在电脑上显示截图
axes_image = plt.imshow(get_screen_image(), animated=True)
figure.canvas.mpl_connect('button_press_event', on_click)
ani = FuncAnimation(figure, update_screen, interval=50, blit=True)
plt.show()
#get_screen_image()