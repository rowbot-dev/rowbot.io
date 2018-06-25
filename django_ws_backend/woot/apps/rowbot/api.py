
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from util.merge import merge
from util.api import Schema, DefaultSchema, types, errors

# from apps.logger.models import SocketLogger
from apps.rowbot.models import (
  AssetModel, Asset, AssetInstance,
  Club,
  EventModel, EventNotificationModel, Event, EventInstance, EventNotification,
  Member, AuthenticationToken,
  RoleModel, RolePermission, Role, RoleInstance, RoleRecord,
  TeamModel, Team, TeamInstance, TeamRecord,
)

class ModelSchema(Schema):
  def __init__(self, model):
    pass

  def query(self, payload):
    pass

api = Schema(
  description='',
  children=merge(
    DefaultSchema().children,
    {
      'models': Schema(
        description='',
        children={
          Model.__name__: ModelSchema(Model) for Model in [
            AssetModel, Asset, AssetInstance,
            Club,
            EventModel, EventNotificationModel, Event, EventInstance, EventNotification,
            Member, AuthenticationToken,
            RoleModel, RolePermission, Role, RoleInstance, RoleRecord,
            TeamModel, Team, TeamInstance, TeamRecord,
          ]
        },
      ),
      'system': Schema(
        description='',
        children={

        },
      ),
    },
  ),
)

ROWBOT = 'rowbot'

class Consumer(JsonWebsocketConsumer):
  groups = []

  def connect(self):
    async_to_sync(self.channel_layer.group_add)(ROWBOT, self.channel_name)
    self.accept()

    response = api.greeting()
    self.send_json(response.render())

    # SocketLogger.objects.connect()

  def receive_json(self, payload):
    response = api.query(payload)
    self.send_json(response.render())

    # SocketLogger.objects.receive()

  def disconnect(self, close_code):
    async_to_sync(self.channel_layer.group_discard)(ROWBOT, self.channel_name)
    print(close_code)

    # SocketLogger.objects.disconnect()

  # channel layer
  def rowbot_send(self, event):
    self.send_json(event.get('data'))

    # SocketLogger.objects.send()
