
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from apps.rowbot.api import query
from apps.rowbot.util import send

class Consumer(JsonWebsocketConsumer):
  groups = ['test']

  def connect(self):
    async_to_sync(self.channel_layer.group_add)('api', self.channel_name)
    self.accept()

  def receive_json(self, payload):
    message_id = payload['context']['message']

    send({
      'id': message_id,
      'data': {
        'key': 'hello back',
      }
    })

  def disconnect(self, close_code):
    async_to_sync(self.channel_layer.group_discard)('api', self.channel_name)
    print(close_code)

  # channel layer
  def api_send(self, event):
    self.send_json(event['data'])
