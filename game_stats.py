# 跟踪游戏的统计信息
class GameStats:

    # 初始化统计信息
    def __init__(self,ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        # 游戏刚启动时处于活动状态
        self.game_active = False
        # 任何情况下都不应重置最高得分
        self.high_score = 0

    # 初始化在游戏运行期间可能变化的统计信息
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.load_high_score()

	def save_high_score(self):
	    f = open("high_score.pkl",'wb')
	    pickle.dump(str(self.high_score),f,0)
	    f.colse()
    
	def load_high_score(self):
	    f = open("high_score.pkl",'rb')
	    try:
                str_high_score = pickle.load(f)
                self.high_score = int(str_high_score)
            except EOFError:
                self.high_score = 0
            finally:
                f.colse()    

    
