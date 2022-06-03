import sys
import pygame

from matplotlib.style import available
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

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
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        # 初始化一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        # 创建记分牌
        self.sb = Scoreboard(self)

        self._create_fleet()

        # 创建play按钮
        self.play_button = Button(self,"PLAY")

    
    # 游戏主循环
    def run_game(self):
        while True:
            # 事件管理循环
            self._check_events()

            if self.stats.game_active:
                # 调用飞船
                self.ship.update()
                # 子弹
                self._update_bullets()
                # 更新外星人位置
                self._update_aliens()
            # 更新屏幕
            self._update_screen()
            

    # 响应按键和鼠标事件
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stats.save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    # 在玩家单机PLAY按钮时开始新游戏
    def _check_play_button(self,mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置游戏统计信息
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

    # 响应按键
    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    # 响应松开
    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    # 创建一颗子弹，并将其加入编组bullets中
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    # 更新子弹的位置并删除消失子弹
    def _update_bullets(self):
        # 更新子弹位置
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        self._check_bullet_alien_collisions()
    
    # 响应子弹和外星人碰撞
    def _check_bullet_alien_collisions(self):
        # 删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # 删除现有的子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()
     
    # 更新外星人群中所有外星人的位置
    def _update_aliens(self):
        # 检查是否有外星人位于屏幕边缘并更新整群外星人的位置
        self._check_fleet_edges()
        self.aliens.update()
        
        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            # print('Ship hit!!!')
            self._ship_hit()
        
        # 检测是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    # 更新屏幕上的图像，并切换到新屏幕
    def _update_screen(self):
        # 每次循环时都要重绘屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态就绘制PLAY按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()

    # 创建外星人群
    def _create_fleet(self):
        # 创建一个外星人并计算一行可容纳多少个外星人
        # 外星人的间距为外星人的宽度
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群
        for  row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)
    
    # 创建一个外星人并将其放在当前行
    def _create_alien(self,alien_number,row_number):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    # 有外星人到达边缘时采取相应的措施
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    # 将整群外星人下移并改变他们的方向
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # 响应飞船被外星人撞到
    def _ship_hit(self):
        # 将ship_left-1
        if self.stats.ships_left > 0:
            # 将ships_left-1并更新记分牌
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，将飞船放到屏幕底端的中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    # 检查是否有外星人到达了屏幕底端
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
