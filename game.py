class Game:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [['.' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'Black'
        self.history = []  # 保存历史状态（每次落子前保存）
        self.pass_count = 0  # 连续虚着次数

    def display_board(self):
        print("\n当前棋盘：")
        for row in self.board:
            print(" ".join(row))

    def save_state(self):
        # 保存当前棋盘状态和当前玩家，以支持悔棋
        self.history.append((self.current_player, [row.copy() for row in self.board]))

    def undo_move(self):
        if self.history:
            # 恢复到当前玩家的上一个状态，回到悔棋前的棋盘状态，不切换玩家
            self.current_player, self.board = self.history.pop()
            print(f"{self.current_player}的上一步操作已撤销，请重新落子。")
        else:
            print("无法悔棋，历史记录为空。")

    def switch_player(self):
        # 切换当前玩家
        self.current_player = 'White' if self.current_player == 'Black' else 'Black'

    def reset_board(self):
        # 重置棋盘并清除历史记录
        self.board = [['.' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.history.clear()
        self.current_player = 'Black'
        self.pass_count = 0  # 重置虚着计数
        print("游戏已重新开始。")
        self.display_board()

    def check_game_over(self):
        """
        游戏是否结束的判断
        这个方法由子类重写。基类只提供判断棋盘是否已满等公共方法。
        """
        raise NotImplementedError("check_game_over() 应该由子类实现")
