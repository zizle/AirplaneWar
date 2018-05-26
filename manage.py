# _*_ coding:utf-8 _*_
from window import GameWindow


if __name__ == '__main__':
    while True:
        # create a window
        window = GameWindow()
        # handing the event in window
        window.event_handler()
        # 显示对象
        window.draw()
        # 刷新窗口
        window.update()
