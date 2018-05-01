
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()
channel_layer_group_send = async_to_sync(channel_layer.group_send)

def send(data):
  channel_layer_group_send('api', {
    'type': 'api.send',
    'data': data,
  })
