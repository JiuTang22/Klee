import pygame
from pygame.sprite import Sprite

# 管理飞船所发射子弹的类
class Bullet(Sprite):

    # 在飞船当前位置创建一个子弹对象
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

    # 向上移动子弹
    def update(self):
        # 更新表示子弹位置的小数值
        self.y -= self.settings.bullet_speed
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    # 在屏幕上绘制子弹
    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
