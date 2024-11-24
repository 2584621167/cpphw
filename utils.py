import json

def save_game(board, current_player, game_type, filename="game_save.json"):
    try:
        game_data = {
            "board": board,
            "current_player": current_player,
            "game_type": game_type
        }
        with open(filename, 'w') as file:
            json.dump(game_data, file)
        print(f"游戏已成功保存至 {filename}")
    except IOError as e:
        print(f"保存失败，发生文件错误: {e}")

def load_game(filename="game_save.json"):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data['board'], data['current_player'], data['game_type']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"存档文件不存在或损坏: {e}")
        return None, None, None
