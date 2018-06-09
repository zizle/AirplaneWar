# _*_ coding:utf-8 _*_

# 掉级敌机强度与我军强度均不改变

import pygame
import random
import time
import threading

WIDTH = 512
HEIGHT = 768


class GameWindow(object):
    """游戏窗口类"""
    def __init__(self):
        """构造方法"""
        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption('AirPlane_War From Zizle')
        # 加载图标
        logo = pygame.image.load('res/hero2.png')
        # 设置图标
        pygame.display.set_icon(logo)
        # 初始化得分
        self.blood = 10

        # 创建文字对象
        self.text = Text()

        # 创建声音对象
        self.sound = Sounds()
        # 播放
        self.sound.bg_play()

        # 创建地图对象
        self.map = Map()

        # 创建英雄飞机
        self.hero_plane = HeroPlane()
        # 装备子弹
        self.hero_plane.equipped_bullet()

        # 创建敌机
        # self.enemy_plane_list = [EnemyPlane() for _ in range(7)]
        self.enemy_plane_list = []
        for _ in range(2):
            self.enemy_plane = EnemyPlane()
            self.enemy_plane_list.append(self.enemy_plane)
        # 装备子弹
        for enemy_plane in self.enemy_plane_list:
            enemy_plane.equipped_bullet()

    def draw(self):
        """显示对象"""
        # 显示背景图片, 不同分数显示不同背景
        # 第一关收获500血晋级
        if self.blood <= 500:
            self.window.blit(self.map.backdrop_img1_1, (self.map.backdrop1_1_rect[0], self.map.backdrop1_1_rect[1]))
            self.window.blit(self.map.backdrop_img1_2, (self.map.backdrop1_2_rect[0], self.map.backdrop1_2_rect[1]))
            # 改变文字并显示文字
            self.text.change_text('第一关', R=155, G=255, B=155)
            self.window.blit(self.text.font_obj, (400, 10))
        # 第二关收获800血晋级
        elif 500 < self.blood <= 1300:
            self.window.blit(self.map.backdrop_img2_1, (self.map.backdrop2_1_rect[0], self.map.backdrop2_1_rect[1]))
            self.window.blit(self.map.backdrop_img2_2, (self.map.backdrop2_2_rect[0], self.map.backdrop2_2_rect[1]))
            # 改变文字并显示文字
            self.text.change_text('第二关', R=255, G=155, B=155)
            self.window.blit(self.text.font_obj, (400, 10))
        # 第三关收获1500血晋级
        elif 1300 < self.blood <= 2800:
            self.window.blit(self.map.backdrop_img3_1, (self.map.backdrop3_1_rect[0], self.map.backdrop3_1_rect[1]))
            self.window.blit(self.map.backdrop_img3_2, (self.map.backdrop3_2_rect[0], self.map.backdrop3_2_rect[1]))
            # 改变文字并显示文字
            self.text.change_text('第三关', R=255, G=255, B=155)
            self.window.blit(self.text.font_obj, (400, 10))
        # 第四关收获2200血晋级
        elif 2800 < self.blood <= 5000:
            self.window.blit(self.map.backdrop_img4_1, (self.map.backdrop4_1_rect[0], self.map.backdrop4_1_rect[1]))
            self.window.blit(self.map.backdrop_img4_2, (self.map.backdrop4_2_rect[0], self.map.backdrop4_2_rect[1]))
            # 改变文字并显示文字
            self.text.change_text('第四关', R=255, G=255, B=155)
            self.window.blit(self.text.font_obj, (400, 10))
        # 第五关终极关
        elif self.blood > 5000:
            self.window.blit(self.map.backdrop_img5_1, (self.map.backdrop5_1_rect[0], self.map.backdrop5_1_rect[1]))
            self.window.blit(self.map.backdrop_img5_2, (self.map.backdrop5_2_rect[0], self.map.backdrop5_2_rect[1]))
            # 改变文字并显示文字
            self.text.change_text('第五关', R=255, G=255, B=155)
            self.window.blit(self.text.font_obj, (400, 10))

        # 滚动背景
        self.map.scroll()
        # 改变文字并显示文字
        self.text.change_text('血量:%d' % self.blood)
        self.window.blit(self.text.font_obj, (10, 10))

        # 敌人飞机显示和发射子弹
        for enemy_plane in self.enemy_plane_list:
            # 遍历当前飞机弹夹
            for enemy_bullet in enemy_plane.bullet_clip:
                # 如果是发射状态就显示
                if enemy_bullet.is_shot:
                    # 子弹下移
                    enemy_bullet.move_down(enemy_plane.speed)
                    self.window.blit(enemy_bullet.enemy_bullet_img, (enemy_bullet.enemy_bullet_rect[0], enemy_bullet.enemy_bullet_rect[1]))
            # 敌机下移显示
            enemy_plane.move_down()
            self.window.blit(enemy_plane.enemy_img, (enemy_plane.enemy_rect[0], enemy_plane.enemy_rect[1]))
        # 显示英雄飞机
        self.window.blit(self.hero_plane.hero_img, (self.hero_plane.hero_rect[0], self.hero_plane.hero_rect[1]))
        # 显示子弹
        # 遍历列表, 发射状态的才显示
        for bullet in self.hero_plane.bullet_clip:
            if bullet.is_shot:
                bullet.move_up()
                self.window.blit(bullet.hero_bullet_img, (bullet.hero_bullet_rect[0], bullet.hero_bullet_rect[1]))

    def event_handler(self):
        """事件处理方法"""
        # 获取事件列表
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                print('点击了关闭按钮')
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('按了ESC退出')
                    exit()
                elif event.key == pygame.K_SPACE:
                    self.hero_plane.shoot()
                    print('biu~biu~biu~')

        # 获取所有按键的状态
        press_keys = pygame.key.get_pressed()
        if press_keys[pygame.K_UP]:
            self.hero_plane.move_up()
            print('上')
        elif press_keys[pygame.K_DOWN]:
            self.hero_plane.move_down()
            print('下')
        elif press_keys[pygame.K_LEFT]:
            self.hero_plane.move_left()
            print('左')
        elif press_keys[pygame.K_RIGHT]:
            self.hero_plane.move_right()
            print('右')

        # 按c继续游戏
        elif press_keys[pygame.K_c] or press_keys[pygame.K_RETURN]:
            # 飞机和子弹都要重置
            for enemy_plane in self.enemy_plane_list:
                for enemy_bullet in enemy_plane.bullet_clip:
                    # 子弹回收
                    enemy_bullet.is_shot = False
                # 敌机位置重置
                enemy_plane.location_reset()
            # 英雄子弹和飞机重置
            for hero_bullent in self.hero_plane.bullet_clip:
                hero_bullent.is_shot = False
            self.hero_plane.location_reset()

            # 如果是游戏失败, 继续游戏
            if press_keys[pygame.K_c]:
                # 我方子弹速度重置
                for hero_bullent in self.hero_plane.bullet_clip:
                    hero_bullent.bullet_speed = 4
                for enemy_plane in self.enemy_plane_list:
                    enemy_plane.shot_time_interval = random.uniform(4, 7)
                    # 敌机速度重置
                    enemy_plane.speed = random.randint(2, 4)
                # 敌机数量重置
                if len(self.enemy_plane_list) > 2:
                    for _ in range(len(self.enemy_plane_list) - 2):
                        self.enemy_plane_list.pop()
                # 地图滚动速度重置
                self.map.speed = 2
                # 分数重置
                self.blood = 10
                # 返回一个数作为条件判断
                return 0
            # 返回1是进入下一关
            return 1

    def collision_detection(self):
        """碰撞检测"""
        # 检测子弹击中敌机
        # 遍历子弹列表
        for hero_bullet in self.hero_plane.bullet_clip:
            if hero_bullet.is_shot:
                # 遍历敌机列表
                for enemy_plane in self.enemy_plane_list:
                    # 检测碰撞
                    if pygame.Rect.colliderect(hero_bullet.hero_bullet_rect, enemy_plane.enemy_rect):
                        hero_bullet.is_shot = False
                        self.sound.bomb_play()
                        # 获得分数
                        self.blood += 10
                        # 摧毁敌机后，相应敌机的子弹全部回收
                        for enemy_bullet in enemy_plane.bullet_clip:
                            enemy_bullet.is_shot = False
                        # 敌机位置重置
                        enemy_plane.location_reset()
                        # break
        # 检测飞机之间是否相撞
        for enemy_plane in self.enemy_plane_list:
            if pygame.Rect.colliderect(enemy_plane.enemy_rect, self.hero_plane.hero_rect):
                print('撞上啦！')
                self.blood -= 50
                # 敌机重置
                enemy_plane.location_reset()

                # 英雄飞机重置

        # 检测敌机子弹是否击中英雄飞机或英雄子弹
        for enemy_plane in self.enemy_plane_list:
            for enemy_bullet in enemy_plane.bullet_clip:
                if enemy_bullet.is_shot:
                    if pygame.Rect.colliderect(enemy_bullet.enemy_bullet_rect, self.hero_plane.hero_rect):
                        print('击中啦！！')
                        self.blood -= 2
                        enemy_bullet.is_shot = False

                        # 英雄飞机重置

                    # 检测子弹之间是否相撞
                    for hero_bullet in self.hero_plane.bullet_clip:
                        if hero_bullet.is_shot:
                            if pygame.Rect.colliderect(hero_bullet.hero_bullet_rect, enemy_bullet.enemy_bullet_rect):
                                # 获得分数
                                self.blood += 2
                                enemy_bullet.is_shot = False
                                hero_bullet.is_shot = False

    def add_one_enemy(self):
        """添加一架敌机"""
        enemy_plane = EnemyPlane()
        # 新飞机装备子弹
        enemy_plane.equipped_bullet()
        # 放入敌机列表
        self.enemy_plane_list.append(enemy_plane)
        # 修改全部飞机的移动速度和发射子弹时间间隔
        for enemy_plane in self.enemy_plane_list:
            # 飞机位置重置
            enemy_plane.location_reset()
            # 移动速度增加
            enemy_plane.speed += 2
            # 在发射子弹间隔大于0.5才会加速发射
            if enemy_plane.shot_time_interval > 1:
                enemy_plane.shot_time_interval -= 1
        # 增加英雄飞机的子弹速度
        for hero_plane_bullet in self.hero_plane.bullet_clip:
            hero_plane_bullet.bullet_speed += 1.5

        # 第图滚动加快
        self.map.speed += 1.5

    def add_enemy_condition(self):
        """线程执行, 符合条件时添加飞机数"""
        while True:
            if 500 < self.blood <= 1300 and len(self.enemy_plane_list) <= 2:
                self.add_one_enemy()

            elif 1300 < self.blood <= 2800 and len(self.enemy_plane_list) <= 3:
                self.add_one_enemy()

            elif 2800 < self.blood <= 5000 and len(self.enemy_plane_list) <= 4:
                self.add_one_enemy()

            elif self.blood > 5000 and len(self.enemy_plane_list) <= 5:
                self.add_one_enemy()

            # 循环不用那么快, 降低cpu负担
            time.sleep(1)

    def game_interval(self):
        """判断当前游戏条件"""
        if self.blood <= 0:
            self.text.change_text("飞机严重贫血", R=255, G=0, B=0)
            self.window.blit(self.text.font_obj, (150, 320))
            self.text.change_text("按下' c 键'继续游戏")
            self.window.blit(self.text.font_obj, (100, 360))
            self.text.change_text("按下' ESC ' 退出游戏")
            self.window.blit(self.text.font_obj, (100, 400))
            self.sound.bg_music_stop()
        elif self.blood > 0:
            self.text.change_text("按'return'进入下一关", R=255, G=255, B=155)
            self.window.blit(self.text.font_obj, (100, 360))
            self.sound.bg_music_stop()
        # 刷新结果
        self.update()
        while True:
            # 返回1的时候结束循环，游戏继续
            if self.event_handler() == 0:
                self.sound.bg_play()
                # 结束循环，继续游戏
                return
            elif self.event_handler() == 1:
                self.blood += 20
                self.sound.bg_play()
                return

    @staticmethod
    def update():
        pygame.display.update()


class Map(object):
    """地图"""
    def __init__(self):
        # 加载背景图片
        self.backdrop_img1_1 = pygame.image.load('res/img_bg_level_1.jpg')
        self.backdrop_img1_2 = pygame.image.load('res/img_bg_level_1.jpg')

        self.backdrop_img2_1 = pygame.image.load('res/img_bg_level_2.jpg')
        self.backdrop_img2_2 = pygame.image.load('res/img_bg_level_2.jpg')

        self.backdrop_img3_1 = pygame.image.load('res/img_bg_level_3.jpg')
        self.backdrop_img3_2 = pygame.image.load('res/img_bg_level_3.jpg')

        self.backdrop_img4_1 = pygame.image.load('res/img_bg_level_4.jpg')
        self.backdrop_img4_2 = pygame.image.load('res/img_bg_level_4.jpg')

        self.backdrop_img5_1 = pygame.image.load('res/img_bg_level_5.jpg')
        self.backdrop_img5_2 = pygame.image.load('res/img_bg_level_5.jpg')

        # 获取背景图片的矩形对象
        self.backdrop1_1_rect = self.backdrop_img1_1.get_rect()
        self.backdrop1_2_rect = self.backdrop_img1_2.get_rect()

        self.backdrop2_1_rect = self.backdrop_img2_1.get_rect()
        self.backdrop2_2_rect = self.backdrop_img2_2.get_rect()

        self.backdrop3_1_rect = self.backdrop_img3_1.get_rect()
        self.backdrop3_2_rect = self.backdrop_img3_2.get_rect()

        self.backdrop4_1_rect = self.backdrop_img4_1.get_rect()
        self.backdrop4_2_rect = self.backdrop_img4_2.get_rect()

        self.backdrop5_1_rect = self.backdrop_img5_1.get_rect()
        self.backdrop5_2_rect = self.backdrop_img5_2.get_rect()

        # 修改初始位置
        self.backdrop1_1_rect[1] = 0
        self.backdrop1_2_rect[1] = - HEIGHT

        self.backdrop2_1_rect[1] = 0
        self.backdrop2_2_rect[1] = - HEIGHT

        self.backdrop3_1_rect[1] = 0
        self.backdrop3_2_rect[1] = - HEIGHT

        self.backdrop4_1_rect[1] = 0
        self.backdrop4_2_rect[1] = - HEIGHT

        self.backdrop5_1_rect[1] = 0
        self.backdrop5_2_rect[1] = - HEIGHT

        # 设置滚动速度
        self.speed = 1.5

    def scroll(self):
        """不同的血量(关卡), 滚动不同的背景"""
        # 第一关
        if window.blood <= 400:
            self.backdrop1_1_rect.move_ip(0, self.speed)
            self.backdrop1_2_rect.move_ip(0, self.speed)
            if self.backdrop1_1_rect[1] >= HEIGHT:
                print('第一张地图出屏幕')
                self.backdrop1_1_rect[1] = - HEIGHT
            elif self.backdrop1_2_rect[1] >= HEIGHT:
                print('第二张地图出屏幕')
                self.backdrop1_2_rect[1] = - HEIGHT
        # 第二关
        elif 500 < window.blood <= 1000:
            self.backdrop2_1_rect.move_ip(0, self.speed)
            self.backdrop2_2_rect.move_ip(0, self.speed)
            if self.backdrop2_1_rect[1] >= HEIGHT:
                print('第一张地图出屏幕')
                self.backdrop2_1_rect[1] = - HEIGHT
            elif self.backdrop2_2_rect[1] >= HEIGHT:
                print('第二张地图出屏幕')
                self.backdrop2_2_rect[1] = - HEIGHT
        # 第三关
        elif 1300 < window.blood <= 2200:
            self.backdrop3_1_rect.move_ip(0, self.speed)
            self.backdrop3_2_rect.move_ip(0, self.speed)
            if self.backdrop3_1_rect[1] >= HEIGHT:
                print('第一张地图出屏幕')
                self.backdrop3_1_rect[1] = - HEIGHT
            elif self.backdrop3_2_rect[1] >= HEIGHT:
                print('第二张地图出屏幕')
                self.backdrop3_2_rect[1] = - HEIGHT
        # 第四关
        elif 2800 < window.blood <= 4000:
            self.backdrop4_1_rect.move_ip(0, self.speed)
            self.backdrop4_2_rect.move_ip(0, self.speed)
            if self.backdrop4_1_rect[1] >= HEIGHT:
                print('第一张地图出屏幕')
                self.backdrop4_1_rect[1] = - HEIGHT
            elif self.backdrop4_2_rect[1] >= HEIGHT:
                print('第二张地图出屏幕')
                self.backdrop4_2_rect[1] = - HEIGHT
        # 第五关
        elif window.blood > 5000:
            self.backdrop5_1_rect.move_ip(0, self.speed)
            self.backdrop5_2_rect.move_ip(0, self.speed)
            if self.backdrop5_1_rect[1] >= HEIGHT:
                print('第一张地图出屏幕')
                self.backdrop5_1_rect[1] = - HEIGHT
            elif self.backdrop5_2_rect[1] >= HEIGHT:
                print('第二张地图出屏幕')
                self.backdrop5_2_rect[1] = - HEIGHT


class Text(object):
    """文字类"""
    def __init__(self):
        """初始化文字"""
        self.font = pygame.font.Font('jdxsj.TTF', 30)
        self.font.set_bold(1)

    def change_text(self, new_text, R=202, G=235, B=212):
        """更改文字"""
        self.font_obj = self.font.render(new_text, False, (R, G, B))


class Sounds(object):
    """声音类"""
    def __init__(self):
        # 加载背景音乐
        pygame.mixer.music.load('res/bg2.ogg')
        # 加载爆炸音效
        self.bomb = pygame.mixer.Sound('res/baozha.ogg')
        # 加载关卡之间音效
        self.interval_sound = pygame.mixer.Sound('res/interval.wav')
        # 加载游戏结束音效
        self.over_sound = pygame.mixer.Sound('res/gameover.wav')

    def bg_play(self):
        # 循环播放背景音乐
        pygame.mixer.music.play(-1)

    def bg_music_stop(self):
        # 停止播放背景音乐
        pygame.mixer.music.stop()

    def bomb_play(self):
        # 播放爆炸音效
        self.bomb.play()

    def interval_sound_play(self):
        self.interval_sound.play()

    def over_sound_play(self):
        self.over_sound.play()


class HeroPlane(object):
    def __init__(self):
        # 加载飞机图片
        self.hero_img = pygame.image.load('res/hero2.png')
        # 英雄飞机的图片矩形对象
        self.hero_rect = self.hero_img.get_rect()
        # 重置飞机位置
        self.hero_rect[0] = (WIDTH - self.hero_rect[2]) / 2
        self.hero_rect[1] = HEIGHT - 100
        # 飞机装备弹夹
        self.bullet_clip = list()
        # 定义飞机移动速度
        self.speed = 10

    def equipped_bullet(self):
        """装备子弹"""
        # 英雄飞机装备10颗
        for _ in range(8):
            self.bullet_clip.append(Bullet())

    def location_reset(self):
        """位置重置"""
        self.hero_rect[0] = (WIDTH - self.hero_rect[2]) / 2
        self.hero_rect[1] = HEIGHT - 100

    def shoot(self):
        for bullet in self.bullet_clip:
            if not bullet.is_shot:
                # 设置子弹位置
                bullet.hero_bullet_rect[0] = self.hero_rect[0] + ((self.hero_rect[2] - bullet.hero_bullet_rect[2]) / 2)
                bullet.hero_bullet_rect[1] = self.hero_rect[1] - bullet.hero_bullet_rect[3]
                bullet.is_shot = True
                # 每次只发射一颗
                break

    def move_up(self):
        if self.hero_rect[1] > 0:
            self.hero_rect.move_ip(0, -self.speed)

    def move_down(self):
        if self.hero_rect[1] < HEIGHT - 100:
            self.hero_rect.move_ip(0, self.speed)

    def move_left(self):
        if self.hero_rect[0] > 0:
            self.hero_rect.move_ip(-self.speed, 0)

    def move_right(self):
        if self.hero_rect[0] < WIDTH - self.hero_rect[2]:
            self.hero_rect.move_ip(self.speed, 0)


class EnemyPlane(object):
    """敌人飞机"""
    def __init__(self):
        mark_num = random.randint(1, 7)
        # 加载飞机图片
        self.enemy_img = pygame.image.load('res/img-plane_%d.png' % mark_num)
        # 获取矩形对象
        self.enemy_rect = self.enemy_img.get_rect()
        # 移动速度
        self.speed = random.uniform(2.5, 4.5)
        # 发射子弹时间间隔
        self.shot_time_interval = random.uniform(4, 7)
        # 重置位置
        self.enemy_rect[0] = random.randint(0, WIDTH - self.enemy_rect[2])
        self.enemy_rect[1] = - self.enemy_rect[3]
        # 弹夹
        self.bullet_clip = []

    def move_down(self):
        """向下移动"""
        self.enemy_rect.move_ip(0, self.speed)
        if self.enemy_rect[1] >= HEIGHT:
            # 重置位置
            self.enemy_rect[0] = random.randint(0, WIDTH - self.enemy_rect[2])
            self.enemy_rect[1] = 0
            # 再次产生移动速度, 飞机速度才会再变化, 线程判断符合条件修改飞机速度就不能再重新给速度了
            # self.speed = random.randint(4, 10)

    def equipped_bullet(self):
        """装备子弹"""
        # 一架飞机装备3颗
        for _ in range(3):
            self.bullet_clip.append(Bullet())

    def location_reset(self):
        self.enemy_rect[0] = random.randint(0, WIDTH - self.enemy_rect[2])
        self.enemy_rect[1] = - self.enemy_rect[3]

    def shoot(self, plane_list):
        """敌机发射子弹，独立一个线程来做"""
        while True:
            for plane in plane_list:
                for bullet in plane.bullet_clip:
                    if not bullet.is_shot:
                        # 设置子弹的位置 x = 当前飞机x + 飞机宽度/2 - 子弹宽度/2
                        #             y = 当前飞机y + 飞机高度
                        bullet.enemy_bullet_rect[0] = \
                            plane.enemy_rect[0] + (plane.enemy_rect[2] - bullet.enemy_bullet_rect[2])/2
                        bullet.enemy_bullet_rect[1] = \
                            plane.enemy_rect[1] + plane.enemy_rect[3]

                        # 子弹状态为发射
                        bullet.is_shot = True
                        # 每次只发一颗
                        break
            # 设置发射子弹的时间间隔
            time.sleep(self.shot_time_interval)


class Bullet(object):
    def __init__(self):
        # 加载子弹图片
        self.hero_bullet_img = pygame.image.load('res/hero_bullet_7.png')
        # 随机获取子弹编号
        mark_num = random.randint(1, 6)
        # 加载敌机子弹图片
        self.enemy_bullet_img = pygame.image.load('res/bullet_%d.png' % mark_num)
        # 获取子弹的矩形对象
        self.hero_bullet_rect = self.hero_bullet_img.get_rect()
        self.enemy_bullet_rect = self.enemy_bullet_img.get_rect()
        # 初始都是未发射状态
        self.is_shot = False
        # 子弹速度
        self.bullet_speed = 4

    def move_up(self):
        self.hero_bullet_rect.move_ip(0, -self.bullet_speed)
        if self.hero_bullet_rect[1] < 0:
            self.is_shot = False

    def move_down(self, plane_speed):
        # 子弹速度随机地比当前飞机快3~6
        add_speed = random.randint(3, 6)
        self.enemy_bullet_rect.move_ip(0, plane_speed + add_speed)
        if self.enemy_bullet_rect[1] >= HEIGHT:
            self.is_shot = False


if __name__ == '__main__':
    # 初始化pygame
    pygame.init()
    # 创建窗口
    window = GameWindow()

    # 创建线程敌机发射子弹
    shoot_thread = threading.Thread(target=window.enemy_plane.shoot, args=(window.enemy_plane_list,), daemon=True)
    shoot_thread.start()
    # 创建线程判断条件添加敌机
    add_thread = threading.Thread(target=window.add_enemy_condition, daemon=True)
    add_thread.start()

    while True:
        # 血量小于0 游戏结束
        if window.blood < 0:
            window.sound.over_sound_play()
            window.game_interval()
        # 进入第二关
        elif window.blood in range(490, 499):
            window.sound.interval_sound_play()
            window.game_interval()
        elif window.blood in range(1290, 1299):
            window.sound.interval_sound_play()
            window.game_interval()
        elif window.blood in range(2790, 2799):
            window.sound.interval_sound_play()
            window.game_interval()
        elif window.blood in range(4990, 4999):
            window.sound.interval_sound_play()
            window.game_interval()
        window.collision_detection()
        # 显示对象
        window.draw()
        # 处理事件
        window.event_handler()
        # 更新窗口
        window.update()