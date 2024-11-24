from game import Game
from utils import save_game

class Go(Game):
    def __init__(self, board_size=19):
        super().__init__(board_size)
        self.captured_stones = {'Black': 0, 'White': 0}
        self.territory = {'Black': 0, 'White': 0}  # 记录占领的区域

    def start_game(self):
        self.display_board()
        while True:
            move = input(f"{self.current_player}的回合，输入坐标 (行 列)，'pass' 虚着，'undo' 悔棋，'resign' 认输，'restart' 重新开始，'save' 保存: ").strip().lower()

            if move == 'pass':
                print(f"{self.current_player}选择虚着。")
                self.pass_count += 1  # 增加虚着计数
                self.switch_player()

                if self.check_game_over():  # 检查是否游戏结束
                    break
                continue
            elif move == 'resign':
                print(f"{self.current_player}认输！游戏结束。")
                break
            elif move == 'restart':
                self.reset_board()
                continue
            elif move == 'save':
                save_game(self.board, self.current_player, "go")
                continue

            try:
                x, y = map(int, move.split())
                if self.is_valid_move(x, y):
                    self.save_state()  # 保存当前状态
                    self.place_stone(x, y)
                    self.capture_stones(x, y)
                    self.display_board()

                    # 问是否悔棋
                    undo_choice = input(f"是否悔棋？(y/n): ").strip().lower()
                    if undo_choice == 'y':
                        self.undo_move()  # 撤销当前回合
                        continue  # 继续当前玩家下棋

                    # 切换玩家回合
                    self.switch_player()
                else:
                    print("无效的落子位置，请重新输入。")
            except ValueError:
                print("输入格式错误，请输入两个数字 (行 列)。")

    def is_valid_move(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[x][y] == '.'

    def place_stone(self, x, y):
        self.board[x][y] = 'B' if self.current_player == 'Black' else 'W'

    def capture_stones(self, x, y):
        opponent_color = 'W' if self.current_player == 'Black' else 'B'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if self.board[nx][ny] == opponent_color:
                    visited = set()
                    if not self.has_liberty(nx, ny, visited):
                        self.remove_group(nx, ny)

    def check_game_over(self):
        # 游戏是否结束的判定
        if self.pass_count >= 2:
            print("双方连续虚着，游戏结束！")
            self.calculate_score()
            return True
        if all(self.board[x][y] != '.' for x in range(self.board_size) for y in range(self.board_size)):
            print("棋盘已满，游戏结束！")
            self.calculate_score()
            return True
        return False

    def calculate_score(self):
        """
        简单的目数计算方法，返回得分
        """
        black_score = 0
        white_score = 0

        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 'B':
                    black_score += 1
                elif self.board[x][y] == 'W':
                    white_score += 1

        black_score += self.captured_stones['Black']
        white_score += self.captured_stones['White']

        print(f"黑方得分: {black_score}")
        print(f"白方得分: {white_score}")

        if black_score > white_score:
            print("黑方获胜！")
        elif black_score < white_score:
            print("白方获胜！")
        else:
            print("平局！")
