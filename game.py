class Game:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [['.' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'Black'
        self.history = []  # 保存历史状态（每次落子前保存）
        self.pass_count = 0  # 连续虚着次数
        self.show_prompt = True  # 是否显示操作提示

    def display_board(self):
        print("\n当前棋盘：")
        for row in self.board:
            print(" ".join(row))

    def display_prompt(self):
        if self.show_prompt:
            print("\n输入操作说明：")
            print("'resign' - 认输, 'restart' - 重新开始, 'save' - 保存, 'menu' - 返回主菜单, 'pass' - 虚着（围棋）")
            print("'hide' - 隐藏提示, 'show' - 显示提示")

    def save_state(self):
        # 保存当前棋盘状态和当前玩家，以支持悔棋
        self.history.append((self.current_player, [row.copy() for row in self.board]))

    def undo_move(self):
        if self.history:
            self.current_player, self.board = self.history.pop()  # 仅撤销当前玩家的操作
            print(f"{self.current_player}的上一步操作已撤销，请重新落子。")
        else:
            print("无法悔棋，历史记录为空。")

    def switch_player(self):
        self.current_player = 'White' if self.current_player == 'Black' else 'Black'

    def reset_board(self):
        self.board = [['.' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.history.clear()
        self.current_player = 'Black'
        self.pass_count = 0
        print("游戏已重新开始。")
        self.display_board()
