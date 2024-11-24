from gomoku import Gomoku
from go import Go
from utils import load_game


def main():
    print("欢迎来到围棋与五子棋平台")
    while True:
        print("\n1. 开始五子棋对局")
        print("2. 开始围棋对局")
        print("3. 读取存档")
        print("4. 退出游戏")
        choice = input("请选择游戏类型: ")

        if choice == '1':
            board_size = int(input("请输入五子棋棋盘大小 (8-19): "))
            if 8 <= board_size <= 19:
                game = Gomoku(board_size)
                game.start_game()
            else:
                print("无效的棋盘大小，请重新输入。")
        elif choice == '2':
            board_size = int(input("请输入围棋棋盘大小 (8-19): "))
            if 8 <= board_size <= 19:
                game = Go(board_size)
                game.start_game()
            else:
                print("无效的棋盘大小，请重新输入。")
        elif choice == '3':
            board, player, game_type = load_game()
            if board:
                if game_type == "gomoku":
                    game = Gomoku(len(board))
                elif game_type == "go":
                    game = Go(len(board))
                else:
                    print("存档的游戏类型无效。")
                    continue

                game.board = board
                game.current_player = player
                game.start_game()
        elif choice == '4':
            print("感谢使用，再见！")
            break
        else:
            print("输入无效，请重新选择。")


if __name__ == "__main__":
    main()
