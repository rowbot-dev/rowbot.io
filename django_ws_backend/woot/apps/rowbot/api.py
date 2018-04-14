from channels.generic.websocket import JsonWebsocketConsumer

class Consumer(JsonWebsocketConsumer):
  groups = ['test']

  def connect(self):
    self.accept()
    self.send_json({'hello': 'hello'})

  def receive_json(self, content):
    print(content)
    self.send_json({'hello': 'hello1'})

  def disconnect(self, close_code):
    print(close_code)
