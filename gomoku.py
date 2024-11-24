from game import Game
from utils import save_game

class Gomoku(Game):
    def __init__(self, board_size=15):
        super().__init__(board_size)

    def start_game(self):
        while True:
            self.display_board()  # 显示棋盘
            self.display_prompt()  # 显示提示信息
            move = input(f"{self.current_player}的回合，请输入指令或坐标 (行 列): ").strip().lower()

            if move == 'menu':
                print("返回主菜单...")
                break
            elif move == 'resign':
                print(f"{self.current_player}认输！游戏结束。")
                break
            elif move == 'restart':
                self.reset_board()
                continue
            elif move == 'save':
                save_game(self.board, self.current_player, "gomoku")
                continue
            elif move == 'hide':
                self.show_prompt = False  # 隐藏提示
                continue
            elif move == 'show':
                self.show_prompt = True  # 显示提示
                continue
            elif move == 'undo':
                self.undo_move()  # 调用父类的悔棋方法
                self.display_board()
                continue

            try:
                x, y = map(int, move.split())
                if self.is_valid_move(x, y):
                    self.save_state()
                    self.board[x][y] = 'B' if self.current_player == 'Black' else 'W'
                    self.display_board()

                    # 在下完棋后询问是否悔棋
                    undo_choice = input(f"是否悔棋？(y/n): ").strip().lower()
                    if undo_choice == 'y':
                        self.undo_move()  # 撤销当前回合
                        continue  # 继续当前玩家下棋

                    if self.check_winner(x, y):
                        print(f"{self.current_player} 获胜！")
                        break
                    if self.check_draw():
                        print("棋盘已满，平局！")
                        break
                    self.switch_player()
                else:
                    print("无效的落子，请重新输入。")
            except ValueError:
                print("输入格式错误，请输入指令或两个数字 (行 列)。")

    def is_valid_move(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[x][y] == '.'

    def check_winner(self, x, y):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 水平、垂直、斜对角线方向
        for dx, dy in directions:
            count = 1  # 当前棋子算一个
            for dir in [1, -1]:
                for step in range(1, 5):  # 检查最多五个方向
                    nx, ny = x + dir * step * dx, y + dir * step * dy
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] == self.board[x][y]:
                        count += 1
                    else:
                        break
            if count >= 5:  # 五子连珠即为胜利
                return True
        return False

    def check_draw(self):
        # 检查棋盘是否已满
        return all(self.board[x][y] != '.' for x in range(self.board_size) for y in range(self.board_size))
