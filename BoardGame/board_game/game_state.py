from board_game.player import Player
import json

class GameState(object):
    def __init__(self, players_count, player_turn, question):
        self.players_count = players_count
        self.player_turn = player_turn
        self.question = question
        self.type = 'game_state'
        self.colors = ["purple", "blue", "yellow", "borwn"]

    def create_game_state(self):
        self.players_array = []

        for i in range(0, self.players_count):
            self.players_array.append(Player(self.colors[i]).__dict__)

        game_state = {
            'players_count': self.players_count,
            'players_array': self.players_array,
            'player_turn': self.player_turn,
            'question': self.question,
            'type': self.type
        }

        save = json.dumps(game_state)
        file = open('./board_game/game_state.txt', 'w')
        file.write(save)
