import sys
import pygame
from settings import Settings
from ship import Ship

# 管理游戏资源和行为的类
class AlienInvasion:
    
    # 初始化游戏并创建游戏资源
    def __init__(self):
        # 初始化背景设置
        pygame.init()
        self.settings = Settings()
        # 创建显示窗口
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        self.bg_color = (230,230,230)
        self.ship = Ship(self)

    
    # 游戏主循环
    def run_game(self):
        while True:
            # 事件管理循环
            self._check_events()
            # 调用飞船
            self.ship.update()
            # 更新屏幕
            self._update_screen()
            

    # 响应按键和鼠标事件
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    # 响应按键
    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    # 响应松开
    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # 更新屏幕上的图像，并切换到新屏幕
    def _update_screen(self):
        # 每次循环时都要重绘屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # 让最近绘制的屏幕可见
        pygame.display.flip()

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
