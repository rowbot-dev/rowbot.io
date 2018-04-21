from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()
channel_layer_group_send = async_to_sync(channel_layer.group_send)

def send(data):
  channel_layer_group_send('api', {
    'type': 'api.send',
    'data': data,
  })

class Consumer(JsonWebsocketConsumer):
  groups = ['test']

  def connect(self):
    self.accept()
    async_to_sync(self.channel_layer.group_add)('api', self.channel_name)

  def receive_json(self, content):
    print(content)

  def disconnect(self, close_code):
    async_to_sync(self.channel_layer.group_discard)('api', self.channel_name)
    print(close_code)

  # channel layer
  def api_send(self, event):
    self.send_json(
      {
        'data': event['data'],
      }
    )
