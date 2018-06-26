
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from util.merge import merge
from util.api import Schema, DefaultSchema, types, map_type, errors

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
  _attributes = 'attributes'
  _relationships = 'relationships'
  _methods = 'methods'
  _instances = 'instances'
  _filter = 'filter'
  _sort = 'sort'
  _paginate = 'paginate'
  _create = 'create'
  _delete = 'delete'

  def __init__(self, Model, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      self._attributes: Schema(
        description='',
        children={
          field.name: Schema(
            description='',
            server_types=map_type(field.get_internal_type())
          )
          for field in Model._meta.get_fields()
          if not field.is_relation
        }
      ),
      self._relationships: Schema(
        description='',
        children={
          field.name: Schema()
          for field in Model._meta.get_fields()
          if field.is_relation
        }
      ),
      self._methods: Schema(
        description='',
      ),
      self._instances: Schema(
        description='',
      ),
      self._filter: Schema(
        description='',
      ),
      self._sort: Schema(
        description='',
      ),
      self._paginate: Schema(
        description='',
      ),
      self._create: Schema(
        description='',
      ),
      self._delete: Schema(
        description='',
      ),
    }

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
