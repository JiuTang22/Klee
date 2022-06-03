# 单元测试，用于对已实现功能进行自动化测试
# test_1用于测试飞船移动
import threading
import unittest
from unittest.mock import patch
import pygame
from alien_invasion import AlienInvasion
import time

class Test_1(unittest.TestCase): 
    def UP(self):
        # 是否按下↑的测试
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
        self.mock_obj._check_keydown_events(event)
        self.assertEqual(self.mock_obj.ship.moving_up, True)
        # 休眠5秒
        time.sleep(5)
        # 5秒后判断是否超出范围
        self.assertGreaterEqual(self.mock_obj.ship.rect.top, 0)

        # 是否松开↑
        event = pygame.event.Event(pygame.KEYUP, key=pygame.K_UP)
        self.mock_obj._check_keyup_events(event)
        self.assertEqual(self.mock_obj.ship.moving_up, False)
        # 上移测试通过
        print("↑")

    def DOWN(self):
        # 按下↓
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        self.mock_obj._check_keydown_events(event)
        self.assertEqual(self.mock_obj.ship.moving_down, True)
        # 休眠5秒
        time.sleep(5)
        # 5秒后判断是否超出范围,界面底部的值要大于飞船底部的值,否则就是超出界面
        self.assertGreaterEqual(self.mock_obj.screen.get_rect().bottom, self.mock_obj.ship.rect.bottom)

        # 松开↓
        event = pygame.event.Event(pygame.KEYUP, key=pygame.K_DOWN)
        self.mock_obj._check_keyup_events(event)
        self.assertEqual(self.mock_obj.ship.moving_down, False)
        # 下移测试通过
        print("↓")

    def RIGHT(self):
        # 按下→
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        self.mock_obj._check_keydown_events(event)
        self.assertEqual(self.mock_obj.ship.moving_right, True)
        # 休眠5秒
        time.sleep(5)
        # 5秒后判断是否超出范围
        self.assertGreaterEqual(250, self.mock_obj.ship.rect.right)

        # 松开→
        event = pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT)
        self.mock_obj._check_keyup_events(event)
        self.assertEqual(self.mock_obj.ship.moving_right, False)
        # 右移测试通过
        print("→")

    def LEFT(self):
        # 按下←
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
        self.mock_obj._check_keydown_events(event)
        self.assertEqual(self.mock_obj.ship.moving_left, True)
        # 休眠5秒
        time.sleep(5)
        # 5秒后判断是否超出范围,飞船左边要大于0像素,fouze超出页面
        self.assertGreaterEqual(self.mock_obj.ship.rect.left, 0)

        # 松开←
        event = pygame.event.Event(pygame.KEYUP, key=pygame.K_LEFT)
        self.mock_obj._check_keyup_events(event)
        self.assertEqual(self.mock_obj.ship.moving_left, False)
        # 左移测试通过
        print("←")

    @patch("alien_invasion.AlienInvasion")    
    def test(self,mock_game):
        mock_game.return_value = AlienInvasion()
        self.mock_obj = mock_game()

        try:
            t = threading.Thread(target=self.mock_obj.run_game)
            # 启动程序
            t.start()
            # 鼠标单击测试
            self.click_play()
            # 上移测试
            self.UP()
            # 下移测试
            self.DOWN()
            # 右移测试
            self.RIGHT()
            # 左移测试
            self.LEFT()
        except Exception as e:
            print(e)

if __name__ == '__main__':
<<<<<<< HEAD
    unittest.main()
=======
    unittest.main()
>>>>>>> 0a4118bd076ad652fb8ad4dd5d592cc48f0a88b1
