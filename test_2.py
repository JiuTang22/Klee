import threading
import unittest
from unittest.mock import patch
import pygame
from alien_invasion import AlienInvasion
import time

# test_2用于测试飞船功能
class Test_2(unittest.TestCase): 

    def Space(self):
        # 连续按3次space
        for bullet_num in range(1, 4):
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            self.mock_obj._check_keydown_events(event)
            event = pygame.event.Event(pygame.KEYUP, key=pygame.K_SPACE)
            self.mock_obj._check_keyup_events(event)
            # 休眠0.2秒,继续
            time.sleep(0.2)
        # 当前应该是正确子弹数
        # 子弹数量是否等于num
        self.assertEqual(len(self.mock_obj.bullets), bullet_num)
        # 子弹测试通过
        print("bullet")

    def ship_hit(self):
        # 模拟飞船被击中
        self.mock_obj._ship_hit()
        # 被击中一次,飞船数量-1
        self.assertEqual(self.mock_obj.stats.ships_left, 2)
        # 飞船碰撞测试通过
        print("pass")
    
    def quit(self):
        # 模拟按下"Q"键
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q)
        self.mock_obj._check_keydown_events(event)
        self.assertEqual(self.mock_obj.end_game, True)
        event = pygame.event.Event(pygame.KEYUP, key=pygame.K_q)
        # 退出游戏测试通过
        print("QUIT")

    def click_play(self):
        # 模拟按下play
        pygame.mouse.set_pos(773,455)
        mouse_pos = pygame.mouse.get_pos()
        self.mock_obj._check_play_button(mouse_pos)
        self.assertEqual(self.mock_obj.stats.game_active, True)
        # 点击PLAY开始游戏测试通过
        print("PLAY")

    @patch("alien_invasion.AlienInvasion")    
    def test(self,mock_game):
        mock_game.return_value = AlienInvasion()
        self.mock_obj = mock_game()

        try:
            t = threading.Thread(target=self.mock_obj.run_game)
            # 启动程序
            t.start()
            # 子弹测试
            self.Space()
            # 飞船碰撞测试
            self.ship_hit()
            # q键退出游戏测试
            self.quit()
            # 点击PLAY开始游戏测试
            self.click_play()

        except Exception as e:
            print(e)


if __name__ == '__main__':
    unittest.main()