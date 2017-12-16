
# DRF
from rest_framework import serializers

# Local
from rowbot.models.asset import AssetModel, Asset, AssetInstance
from rowbot.models.club import Club
from rowbot.models.event import EventModel, Event, EventInstance, EventNotification
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
    depth = 1

class AssetSerializer(serializers.ModelSerializer):
  model = UUIDRelatedField(read_only=True)
  parts = UUIDRelatedField(queryset=Asset.objects.all(), many=True)
  is_part_of = UUIDRelatedField(queryset=Asset.objects.all(), many=True)
  instances = AssetInstanceSerializer(many=True)

  class Meta:
    model = Asset
    fields = ('_id', '_ref', 'date_created', 'name', 'location', 'description', 'model', 'parts', 'is_part_of', 'instances')
    depth = 1

class AssetModelSerializer(serializers.ModelSerializer):
  club = UUIDRelatedField(read_only=True)
  parts = UUIDRelatedField(queryset=AssetModel.objects.all(), many=True)
  is_part_of = UUIDRelatedField(queryset=AssetModel.objects.all(), many=True)
  assets = AssetSerializer(many=True)

  class Meta:
    model = AssetModel
    fields = ('_id', '_ref', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'club', 'parts', 'is_part_of', 'assets')
    depth = 1

# Role
class RolePermissionSerializer(serializers.ModelSerializer):
  models = UUIDRelatedField(queryset=RoleModel.objects.all(), many=True)

  class Meta:
    model = RolePermission
    fields = ('_id', '_ref', 'date_created', 'model_name', 'name', 'models')
    depth = 1

class RoleInstanceSerializer(serializers.ModelSerializer):
  role = UUIDRelatedField(read_only=True)
  event = UUIDRelatedField(read_only=True)

  class Meta:
    model = RoleInstance
    fields = ('_id', '_ref', 'date_created', 'role', 'event')
    depth = 1

class RoleRecordSerializer(serializers.ModelSerializer):
  role = UUIDRelatedField(read_only=True)
  event = UUIDRelatedField(read_only=True)

  class Meta:
    model = RoleRecord
    fields = ('_id', '_ref', 'date_created', 'role', 'event')
    depth = 1

class RoleSerializer(serializers.ModelSerializer):
  team = UUIDRelatedField(read_only=True)
  model = UUIDRelatedField(read_only=True)
  member = UUIDRelatedField(read_only=True)
  is_superior_to = UUIDRelatedField(queryset=Role.objects.all(), many=True)
  is_subordinate_to = UUIDRelatedField(queryset=Role.objects.all(), many=True)
  instances = RoleInstanceSerializer(many=True)
  records = RoleRecordSerializer(many=True)

  class Meta:
    model = Role
    fields = ('_id', '_ref', 'date_created', 'nickname', 'team', 'model', 'member', 'is_superior_to', 'is_subordinate_to', 'instances', 'records')
    depth = 1

class RoleModelSerializer(serializers.ModelSerializer):
  club = UUIDRelatedField(queryset=Club.objects.all())
  is_superior_to = UUIDRelatedField(queryset=RoleModel.objects.all(), many=True)
  is_subordinate_to = UUIDRelatedField(queryset=RoleModel.objects.all(), many=True)
  permissions = UUIDRelatedField(queryset=RolePermission.objects.all(), many=True)
  roles = RoleSerializer(many=True)

  class Meta:
    model = RoleModel
    fields = ('_id', '_ref', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'club', 'is_superior_to', 'is_subordinate_to', 'permissions', 'roles')
    depth = 1

# Team
class TeamInstanceSerializer(serializers.ModelSerializer):
  team = UUIDRelatedField(read_only=True)
  event = UUIDRelatedField(read_only=True)

  class Meta:
    model = TeamInstance
    fields = ('_id', '_ref', 'date_created', 'team', 'event')
    depth = 1

class TeamRecordSerializer(serializers.ModelSerializer):
  team = UUIDRelatedField(read_only=True)
  event = UUIDRelatedField(read_only=True)

  class Meta:
    model = TeamRecord
    fields = ('_id', '_ref', 'date_created', 'team', 'event')
    depth = 1

class TeamSerializer(serializers.ModelSerializer):
  model = UUIDRelatedField(read_only=True)
  is_superset_of = UUIDRelatedField(queryset=Team.objects.all(), many=True)
  is_subset_of = UUIDRelatedField(queryset=Team.objects.all(), many=True)
  instances = TeamInstanceSerializer(many=True)
  records = TeamRecordSerializer(many=True)
  assets = AssetInstanceSerializer(many=True)
  roles = RoleSerializer(many=True)

  class Meta:
    model = Team
    fields = ('_id', '_ref', 'date_created', 'name', 'club', 'model', 'is_superset_of', 'is_subset_of', 'instances', 'records', 'assets', 'roles')
    depth = 1

class TeamModelSerializer(serializers.ModelSerializer):
  club = UUIDRelatedField(read_only=True)
  is_superset_of = UUIDRelatedField(queryset=TeamModel.objects.all(), many=True)
  is_subset_of = UUIDRelatedField(queryset=TeamModel.objects.all(), many=True)
  teams = TeamSerializer(many=True)

  class Meta:
    model = TeamModel
    fields = ('_id', '_ref', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'club', 'is_superset_of', 'is_subset_of', 'teams')
    depth = 1

# Event
class EventNotificationSerializer(serializers.ModelSerializer):
  event = UUIDRelatedField(read_only=True)

  class Meta:
    model = EventNotification
    fields = ('_id', '_ref', 'date_created', 'event', 'schedule_id', 'timestamp', 'is_active')
    depth = 1

class EventInstanceSerializer(serializers.ModelSerializer):
  event = UUIDRelatedField(read_only=True)
  teams = TeamInstanceSerializer(many=True)

  class Meta:
    model = EventInstance
    fields = ('_id', '_ref', 'date_created', 'description', 'event', 'teams', 'is_active')
    depth = 1

  # override save method
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    # run method to update scheduler
    self.instance.schedule()

class EventSerializer(serializers.ModelSerializer):
  model = UUIDRelatedField(read_only=True)
  parts = UUIDRelatedField(queryset=Event.objects.all(), many=True)
  is_part_of = UUIDRelatedField(queryset=Event.objects.all(), many=True)
  instances = EventInstanceSerializer(many=True)

  class Meta:
    model = Event
    fields = ('_id', '_ref', 'date_created', 'name', 'description', 'model', 'parts', 'is_part_of', 'instances')
    depth = 1

class EventRepeatSerializer(serializers.Serializer):
  interval = serializers.DurationField()

class EventModelSerializer(serializers.ModelSerializer):
  club = UUIDRelatedField(read_only=True)
  parts = UUIDRelatedField(queryset=EventModel.objects.all(), many=True)
  is_part_of = UUIDRelatedField(queryset=EventModel.objects.all(), many=True)
  events = EventSerializer(many=True)

  class Meta:
    model = EventModel
    fields = ('_id', '_ref', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'club', 'parts', 'is_part_of', 'events', 'is_active')
    depth = 1

# Club
class ClubSerializer(serializers.ModelSerializer):
  asset_models = AssetModelSerializer(many=True)
  role_models = RoleModelSerializer(many=True)
  team_models = TeamModelSerializer(many=True)
  event_models = EventModelSerializer(many=True)

  class Meta:
    model = Club
    fields = ('_id', '_ref', 'date_created', 'name', 'asset_models', 'role_models', 'team_models', 'event_models')
    depth = 1

# Member
class MemberSerializer(serializers.ModelSerializer):
  roles = RoleSerializer(many=True)

  class Meta:
    model = Member
    fields = ('_id', '_ref', 'date_created', 'username', 'email', 'first_name', 'last_name', 'is_activated', 'is_enabled', 'is_staff', 'roles')
    depth = 1
