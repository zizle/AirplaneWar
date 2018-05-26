# _*_ coding:utf-8 _*_
import pygame
from config import WIDTH, HEIGHT, HERO_SPEED


class Hero(object):
    def __init__(self):
        # 加载飞机图片
        self.hero_img = pygame.image.load('res/hero2.png')
        # 英雄飞机的图片矩形对象
        self.hero_rect = self.hero_img.get_rect()
        # 重置飞机位置
        self.hero_rect[0] = (WIDTH - self.hero_rect[2]) / 2
        self.hero_rect[1] = HEIGHT - 100

    def move_up(self):
        if self.hero_rect[1] > 0:
            self.hero_rect.move_ip(0, -HERO_SPEED)

    def move_down(self):
        if self.hero_rect[1] < HEIGHT - 100:
            self.hero_rect.move_ip(0, HERO_SPEED)

    def move_left(self):
        if self.hero_rect[0] > 0:
            self.hero_rect.move_ip(-HERO_SPEED, 0)

    def move_right(self):
        if self.hero_rect[0] < WIDTH - self.hero_rect[2]:
                self.hero_rect.move_ip(HERO_SPEED, 0)


# 实例化英雄飞机对象
hero_plane = Hero()
