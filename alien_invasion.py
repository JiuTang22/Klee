import sys
import pygame

# 管理游戏资源和行为的类
class AlienInvasion:
    
    # 初始化游戏并创建游戏资源
    def __init__(self):
        # 初始化背景设置
        pygame.init()
        # 创建显示窗口
        self.screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption('Alien Invasion')
    
    # 游戏主循环
    def run_game(self):
        while True:
            # 监听键盘和鼠标事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit
            # 让最近绘制的屏幕可见
            pygame.display.flip()

if __name__ == '_main_':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
