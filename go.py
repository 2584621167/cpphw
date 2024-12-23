from game import Game
from utils import save_game

class Go(Game):
    def __init__(self, board_size=19):
        super().__init__(board_size)
        self.captured_stones = {'Black': 0, 'White': 0}

    def start_game(self):
        while True:
            self.display_board()  # 显示棋盘
            self.display_prompt()  # 显示提示信息
            move = input(f"{self.current_player}的回合，请输入指令或坐标 (行 列): ").strip().lower()

            if move == 'pass':
                print(f"{self.current_player}选择虚着。")
                self.pass_count += 1
                if self.check_game_over():
                    break
                self.switch_player()
                continue
            elif move == 'menu':
                print("返回主菜单...")
                break
            elif move == 'resign':
                print(f"{self.current_player}认输！游戏结束。")
                print(f"{'白方' if self.current_player == 'Black' else '黑方'} 获胜！")
                break
            elif move == 'restart':
                self.reset_board()
                continue
            elif move == 'save':
                save_game(self.board, self.current_player, "go")
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
                    self.save_state()  # 保存状态用于悔棋
                    self.place_stone(x, y)
                    self.capture_stones(x, y)  # 添加提子逻辑
                    self.display_board()

                    # 在下完棋后询问是否悔棋
                    undo_choice = input(f"是否悔棋？(y/n): ").strip().lower()
                    if undo_choice == 'y':
                        self.undo_move()  # 撤销当前回合
                        continue  # 继续当前玩家下棋

                    self.switch_player()
                else:
                    print("无效的落子位置，请重新输入。")
            except ValueError:
                print("输入格式错误，请输入指令或两个数字 (行 列)。")

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

    def has_liberty(self, x, y, visited):
        if (x, y) in visited:
            return False
        visited.add((x, y))

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if self.board[nx][ny] == '.':
                    return True  # 发现有气
                if self.board[nx][ny] == self.board[x][y] and self.has_liberty(nx, ny, visited):
                    return True
        return False

    def remove_group(self, x, y):
        color = self.board[x][y]
        self.board[x][y] = '.'
        self.captured_stones['Black' if color == 'W' else 'White'] += 1  # 提子计数

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] == color:
                self.remove_group(nx, ny)  # 递归移除整个棋子组

    def check_game_over(self):
        if self.pass_count >= 2:
            print("双方连续虚着，游戏结束！")
            self.calculate_score()  # 计算并显示最终得分
            return True
        if all(self.board[x][y] != '.' for x in range(self.board_size) for y in range(self.board_size)):
            print("棋盘已满，游戏结束！")
            self.calculate_score()
            return True
        return False

    def calculate_score(self):
        visited = set()
        black_score = self.captured_stones['Black']
        white_score = self.captured_stones['White']

        def dfs(x, y, color):
            if (x, y) in visited:
                return 0
            visited.add((x, y))
            score = 1
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.board[nx][ny] == color:
                        score += dfs(nx, ny, color)
            return score

        for x in range(self.board_size):
            for y in range(self.board_size):
                if (x, y) not in visited:
                    if self.board[x][y] == 'B':
                        black_score += dfs(x, y, 'B')
                    elif self.board[x][y] == 'W':
                        white_score += dfs(x, y, 'W')

        print(f"黑方得分: {black_score}")
        print(f"白方得分: {white_score}")

        if black_score > white_score:
            print("黑方获胜！")
        elif black_score < white_score:
            print("白方获胜！")
        else:
            print("平局！")
