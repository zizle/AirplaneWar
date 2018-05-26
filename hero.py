# _*_ coding:utf-8 _*_
import pygame
from config import WIDTH, HEIGHT


class Hero(object):
    def __init__(self):
        # 加载飞机图片
        self.hero_img = pygame.image.load('res/hero2.png')
        # 英雄飞机的图片矩形对象
        self.hero_rect = self.hero_img.get_rect()
        # 重置飞机位置
        self.hero_rect[0] = (WIDTH - self.hero_rect[2]) / 2
        self.hero_rect[1] = HEIGHT - 100


# 实例化英雄飞机对象
hero_plane = Hero()
