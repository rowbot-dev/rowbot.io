
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from util.merge import merge
from util.api import StructureSchema, types, map_type, errors

# from apps.logger.models import SocketLogger
from apps.base.schema import ModelsSchemaWithReferences
from apps.reference.models import Reference
from apps.rowbot.models import (
  AssetModel, Asset, AssetInstance,
  Club,
  EventModel, EventNotificationModel, Event, EventInstance, EventNotification,
  Member, AuthenticationToken,
  RoleModel, RolePermission, Role, RoleInstance, RoleRecord,
  TeamModel, Team, TeamInstance, TeamRecord,
)

class api_constants:
  MODELS = 'models'
  SYSTEM = 'system'

api = StructureSchema(
  description='',
  children={
    api_constants.MODELS: ModelsSchemaWithReferences(
      reference_group_model=Reference,
      description='',
      children={
        Model.__name__: Model.objects.schema() for Model in [
          # AssetModel, Asset, AssetInstance,
          # Club,
          # EventModel, EventNotificationModel, Event, EventInstance, EventNotification,
          Member,
          # AuthenticationToken,
          # RoleModel, RolePermission,
          Role,
          # RoleInstance, RoleRecord,
          # TeamModel, Team, TeamInstance, TeamRecord,
        ]
      },
    ),
    api_constants.SYSTEM: StructureSchema(
      description='',
      children={

      },
    ),
  },
)

ROWBOT = 'rowbot'

class Consumer(JsonWebsocketConsumer):
  groups = []

  def connect(self):
    async_to_sync(self.channel_layer.group_add)(ROWBOT, self.channel_name)
    self.accept()

    response = api.empty()
    self.send_json(response.empty())

    # SocketLogger.objects.connect()

  def receive_json(self, payload):
    response = api.respond(payload)
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
