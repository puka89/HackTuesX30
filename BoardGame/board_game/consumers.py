from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "game_room"
        print('connecte')
        self.room_group_name = '%s_group' % self.room_name

        # Join room group
        self.channel_layer.group_add(self.room_group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        self.send_game_state()

    def send_game_state(self):
        game_state = self.get_current_game_state()
        self.channel_layer.groupd_send(
            self.room_group_name,
            { 'message': game_state }
        )

    def render_game_state(self, event):
        game_state = event['message']

        self.send(text_data=json.dumps({
            'game_state': game_state
        }))

    def get_current_game_state(self):
        pass

    def reset_game_state(self, players_count):
        pass
