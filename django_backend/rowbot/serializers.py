
# DRF
from rest_framework import serializers

# Local
from rowbot.models.asset import AssetModel, Asset, AssetInstance
from rowbot.models.club import Club
from rowbot.models.event import EventModel, EventNotificationModel, Event, EventInstance, EventNotification
from rowbot.models.member import Member
from rowbot.models.role import RoleModel, RolePermission, Role, RoleInstance, RoleRecord
from rowbot.models.team import TeamModel, Team, TeamInstance, TeamRecord

class UUIDRelatedField(serializers.PrimaryKeyRelatedField):
  def use_pk_only_optimization(self):
    return False

  def to_representation(self, value):
    return value._ref

# Heirarchy:
# Asset
# Role
# Team
# Event
# Club
# Member

# Asset
class AssetInstanceSerializer(serializers.ModelSerializer):
  asset = UUIDRelatedField(read_only=True)
  team = UUIDRelatedField(queryset=Team.objects.all(), many=True)
  in_possession_of = UUIDRelatedField(queryset=Team.objects.all(), many=True)
  event = UUIDRelatedField(read_only=True)

  class Meta:
    model = AssetInstance
    fields = ('_id', '_ref', 'date_created', 'metadata', 'asset', 'team', 'in_possession_of', 'event')

class AssetSerializer(serializers.ModelSerializer):
  model = UUIDRelatedField(read_only=True)
  parts = UUIDRelatedField(queryset=Asset.objects.all(), many=True)
  is_part_of = UUIDRelatedField(queryset=Asset.objects.all(), many=True)
  instances = UUIDRelatedField(queryset=AssetInstance.objects.all(), many=True)

  class Meta:
    model = Asset
    fields = ('_id', '_ref', 'date_created', 'name', 'location', 'description', 'model', 'parts', 'is_part_of', 'instances')

class AssetModelSerializer(serializers.ModelSerializer):
  club = UUIDRelatedField(read_only=True)
  parts = UUIDRelatedField(queryset=AssetModel.objects.all(), many=True)
  is_part_of = UUIDRelatedField(queryset=AssetModel.objects.all(), many=True)
  assets = UUIDRelatedField(queryset=Asset.objects.all(), many=True)

  class Meta:
    model = AssetModel
    fields = ('_id', '_ref', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'club', 'parts', 'is_part_of', 'assets')

# Role
class RolePermissionSerializer(serializers.ModelSerializer):
  models = UUIDRelatedField(queryset=RoleModel.objects.all(), many=True)

  class Meta:
    model = RolePermission
    fields = ('_id', '_ref', 'date_created', 'model_name', 'name', 'models')

class RoleInstanceSerializer(serializers.ModelSerializer):
  role = UUIDRelatedField(queryset=Role.objects.all())
  event = UUIDRelatedField(queryset=EventInstance.objects.all())

  class Meta:
    model = RoleInstance
    fields = ('_id', '_ref', 'date_created', 'is_active', 'is_confirmed', 'role', 'event')

class RoleRecordSerializer(serializers.ModelSerializer):
  role = UUIDRelatedField(read_only=True)
  event = UUIDRelatedField(read_only=True)

  class Meta:
    model = RoleRecord
    fields = ('_id', '_ref', 'date_created', 'role', 'event')

class RoleSerializer(serializers.ModelSerializer):
  team = UUIDRelatedField(queryset=Team.objects.all(), required=False)
  model = UUIDRelatedField(queryset=RoleModel.objects.all())
  member = UUIDRelatedField(queryset=Member.objects.all())
  is_superior_to = UUIDRelatedField(queryset=Role.objects.all(), many=True, required=False)
  is_subordinate_to = UUIDRelatedField(queryset=Role.objects.all(), many=True, required=False)
  instances = UUIDRelatedField(queryset=RoleInstance.objects.all(), many=True, required=False)
  records = UUIDRelatedField(queryset=RoleRecord.objects.all(), many=True, required=False)

  class Meta:
    model = Role
    fields = ('_id', '_ref', 'date_created', 'nickname', 'is_active', 'is_confirmed', 'team', 'model', 'member', 'is_superior_to', 'is_subordinate_to', 'instances', 'records')

class RoleModelSerializer(serializers.ModelSerializer):
  club = UUIDRelatedField(queryset=Club.objects.all())
  is_superior_to = UUIDRelatedField(queryset=RoleModel.objects.all(), many=True)
  is_subordinate_to = UUIDRelatedField(queryset=RoleModel.objects.all(), many=True)
  permissions = UUIDRelatedField(queryset=RolePermission.objects.all(), many=True)
  roles = UUIDRelatedField(queryset=Role.objects.all(), many=True)

  class Meta:
    model = RoleModel
    fields = ('_id', '_ref', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'club', 'is_superior_to', 'is_subordinate_to', 'permissions', 'roles')

# Team
class TeamInstanceSerializer(serializers.ModelSerializer):
  team = UUIDRelatedField(read_only=True) # TODO
  event = UUIDRelatedField(read_only=True)

  class Meta:
    model = TeamInstance
    fields = ('_id', '_ref', 'date_created', 'team', 'event')

class TeamRecordSerializer(serializers.ModelSerializer):
  team = UUIDRelatedField(queryset=TeamInstance.objects.all())
  event = UUIDRelatedField(queryset=EventInstance.objects.all())

  class Meta:
    model = TeamRecord
    fields = ('_id', '_ref', 'date_created', 'team', 'event')

class TeamSerializer(serializers.ModelSerializer):
  model = UUIDRelatedField(queryset=TeamModel.objects.all())
  is_superset_of = UUIDRelatedField(queryset=Team.objects.all(), many=True)
  is_subset_of = UUIDRelatedField(queryset=Team.objects.all(), many=True)
  instances = UUIDRelatedField(queryset=TeamInstance.objects.all(), many=True)
  records = UUIDRelatedField(queryset=TeamRecord.objects.all(), many=True)
  assets = UUIDRelatedField(queryset=AssetInstance.objects.all(), many=True)
  roles = UUIDRelatedField(queryset=Role.objects.all(), many=True)

  class Meta:
    model = Team
    fields = ('_id', '_ref', 'date_created', 'name', 'club', 'model', 'is_superset_of', 'is_subset_of', 'instances', 'records', 'assets', 'roles')

class TeamModelSerializer(serializers.ModelSerializer):
  club = UUIDRelatedField(queryset=Club.objects.all())
  is_superset_of = UUIDRelatedField(queryset=TeamModel.objects.all(), many=True)
  is_subset_of = UUIDRelatedField(queryset=TeamModel.objects.all(), many=True)
  teams = UUIDRelatedField(queryset=Team.objects.all(), many=True)

  class Meta:
    model = TeamModel
    fields = ('_id', '_ref', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'club', 'is_superset_of', 'is_subset_of', 'teams')

# Event
class EventNotificationSerializer(serializers.ModelSerializer):
  event = UUIDRelatedField(read_only=True)

  class Meta:
    model = EventNotification
    fields = ('_id', '_ref', 'date_created', 'event', 'name', 'schedule_id', 'timestamp', 'is_active')

class EventInstanceSerializer(serializers.ModelSerializer):
  event = UUIDRelatedField(queryset=Event.objects.all())
  teams = UUIDRelatedField(queryset=TeamInstance.objects.all(), many=True, required=False)
  roles = UUIDRelatedField(queryset=RoleInstance.objects.all(), many=True, required=False)

  class Meta:
    model = EventInstance
    fields = ('_id', '_ref', 'date_created', 'start_time', 'end_time', 'location', 'description', 'is_active', 'event', 'teams', 'roles')

  # override save method
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    # run method to update scheduler
    self.instance.schedule()

class EventSerializer(serializers.ModelSerializer):
  model = UUIDRelatedField(queryset=EventModel.objects.all())
  parts = UUIDRelatedField(queryset=Event.objects.all(), many=True, required=False)
  is_part_of = UUIDRelatedField(queryset=Event.objects.all(), many=True, required=False)
  instances = UUIDRelatedField(queryset=EventInstance.objects.all(), many=True, required=False)

  class Meta:
    model = Event
    fields = ('_id', '_ref', 'date_created', 'name', 'description', 'model', 'parts', 'is_part_of', 'instances', 'is_active')

class EventRepeatSerializer(serializers.Serializer):
  interval = serializers.DurationField()

class EventNotificationModelSerializer(serializers.ModelSerializer):
  model = UUIDRelatedField(queryset=EventModel.objects.all())

  class Meta:
    model = EventNotificationModel
    fields = ('_id', '_ref', 'date_created', 'name', 'relative_duration', 'is_absolute', 'absolute_hour', 'absolute_minute', 'model')

class EventModelSerializer(serializers.ModelSerializer):
  club = UUIDRelatedField(queryset=Club.objects.all())
  parts = UUIDRelatedField(queryset=EventModel.objects.all(), many=True)
  is_part_of = UUIDRelatedField(queryset=EventModel.objects.all(), many=True)
  events = UUIDRelatedField(queryset=Event.objects.all(), many=True)

  class Meta:
    model = EventModel
    fields = ('_id', '_ref', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'club', 'parts', 'is_part_of', 'events')

# Club
class ClubSerializer(serializers.ModelSerializer):
  asset_models = UUIDRelatedField(queryset=AssetModel.objects.all(), many=True)
  role_models = UUIDRelatedField(queryset=RoleModel.objects.all(), many=True)
  team_models = UUIDRelatedField(queryset=TeamModel.objects.all(), many=True)
  event_models = UUIDRelatedField(queryset=EventModel.objects.all(), many=True)

  class Meta:
    model = Club
    fields = ('_id', '_ref', 'date_created', 'name', 'asset_models', 'role_models', 'team_models', 'event_models')

# Member
class MemberSerializer(serializers.ModelSerializer):
  roles = UUIDRelatedField(queryset=Role.objects.all(), many=True)

  class Meta:
    model = Member
    fields = ('_id', '_ref', 'date_created', 'username', 'email', 'first_name', 'last_name', 'is_activated', 'is_enabled', 'is_staff', 'roles')
