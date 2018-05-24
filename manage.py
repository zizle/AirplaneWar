# _*_ coding:utf-8 _*_
import pygame

WIDTH = 512
HEIGHT = 768


class GameWindow(object):
    def __init__(self):

        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption('AirPlane_War From Zizle')
        # 加载图标
        logo = pygame.image.load('res/hero2.png')
        # 设置图标
        pygame.display.set_icon(logo)
        # 加载资源图片，返回图片对象
        bg_image = pygame.image.load("res/img_bg_level_2.jpg")
        # 指定坐标，将图片绘制到窗口
        self.window.blit(bg_image, (0, 0))
        pygame.display.update()


if __name__ == '__main__':
    # 初始化pygame
    pygame.init()
    # 创建窗口
    window = GameWindow()
    input()

