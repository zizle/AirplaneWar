# _*_ coding:utf-8 _*_
import pygame
from config import WIDTH, HEIGHT
from hero import Hero, hero_plane


# initialize pygame
pygame.init()


class GameWindow(object):
    def __init__(self):
        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption('AirPlane_War From Zizle')
        # loading icon
        logo = pygame.image.load('res/hero2.png')
        # set icon
        pygame.display.set_icon(logo)
        # loading the background image
        bg_image = pygame.image.load("res/img_bg_level_2.jpg")
        # setup image location
        self.window.blit(bg_image, (0, 0))

    def draw(self):
        """绘制对象"""
        # 显示英雄飞机
        self.window.blit(hero_plane.hero_img, (hero_plane.hero_rect[0], hero_plane.hero_rect[1]))

    def event_handler(self):
        """window event handling"""
        # get the event
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                print('click on quit button')
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('Press the ESC')
                    exit()
                elif event.key == pygame.K_SPACE:
                    print('bullets...')

        # get the keyboards status
        press_keys = pygame.key.get_pressed()
        if press_keys[pygame.K_UP]:
            print('Up')
        elif press_keys[pygame.K_DOWN]:
            print('Down')
        elif press_keys[pygame.K_LEFT]:
            print('Left')
        elif press_keys[pygame.K_RIGHT]:
            print('Right')

    @staticmethod
    def update():
        """刷新窗口"""
        # refresh the window
        pygame.display.update()
