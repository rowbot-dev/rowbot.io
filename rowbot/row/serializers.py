
# DRF
from rest_framework import serializers

# Local
from row.models.asset import AssetModel, Asset, AssetInstance
from row.models.club import Club
from row.models.event import EventModel, Event, EventInstance
from row.models.member import Member
from row.models.role import RoleModel, RolePermission, Role, RoleInstance, RoleRecord
from row.models.team import TeamModel, Team, TeamInstance, TeamRecord

# Heirarchy:
# Asset
# Role
# Team
# Event
# Club
# Member

# Asset
class AssetModelSerializer(serializers.ModelSerializer):
  club = serializers.PrimaryKeyRelatedField(read_only=True)
  parts = serializers.PrimaryKeyRelatedField(queryset=AssetModel.objects.all())
  is_part_of = serializers.PrimaryKeyRelatedField(queryset=AssetModel.objects.all())

  class Meta:
    model = AssetModel
    fields = ('_id', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'club', 'parts', 'is_part_of')

class AssetInstanceSerializer(serializers.ModelSerializer):
  asset = serializers.PrimaryKeyRelatedField(read_only=True)
  team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
  in_possession_of = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

  class Meta:
    model = AssetInstance
    fields = ('_id', 'date_created', 'metadata', 'asset', 'team', 'in_possession_of')

class AssetSerializer(serializers.ModelSerializer):
  model = serializers.PrimaryKeyRelatedField(read_only=True)
  parts = serializers.PrimaryKeyRelatedField(queryset=Asset.objects.all())
  is_part_of = serializers.PrimaryKeyRelatedField(queryset=Asset.objects.all())
  instances = AssetInstanceSerializer(many=True)

  class Meta:
    model = Asset
    fields = ('_id', 'date_created', 'name', 'location', 'description', 'model', 'parts', 'is_part_of', 'instances')

# Role
class RoleModelSerializer(serializers.ModelSerializer):
  club = serializers.PrimaryKeyRelatedField(queryset=Club.objects.all())
  is_superior_to = serializers.PrimaryKeyRelatedField(queryset=RoleModel.objects.all())
  is_subordinate_to = serializers.PrimaryKeyRelatedField(queryset=RoleModel.objects.all())
  permissions = serializers.PrimaryKeyRelatedField(queryset=RolePermission.objects.all())

  class Meta:
    model = RoleModel
    fields = ('_id', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'club', 'is_superior_to', 'is_subordinate_to')

class RolePermissionSerializer(serializers.ModelSerializer):
  models = serializers.PrimaryKeyRelatedField(queryset=RoleModel.objects.all())

  class Meta:
    model = RolePermission
    fields = ('_id', 'date_created', 'model_name', 'name', 'models')

class RoleInstanceSerializer(serializers.ModelSerializer):
  role = serializers.PrimaryKeyRelatedField(read_only=True)
  event = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = RoleInstance
    fields = ('_id', 'date_created', 'role', 'event')

class RoleRecordSerializer(serializers.ModelSerializer):
  role = serializers.PrimaryKeyRelatedField(read_only=True)
  event = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = RoleRecord
    fields = ('_id', 'date_created', 'role', 'event')

class RoleSerializer(serializers.ModelSerializer):
  team = serializers.PrimaryKeyRelatedField(read_only=True)
  model = serializers.PrimaryKeyRelatedField(read_only=True)
  member = serializers.PrimaryKeyRelatedField(read_only=True)
  is_superior_to = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
  is_subordinate_to = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
  instances = RoleInstanceSerializer(many=True)
  records = RoleRecordSerializer(many=True)

  class Meta:
    model = Role
    fields = ('_id', 'date_created', 'nickname', 'club', 'team', 'type', 'member', 'is_superior_to', 'is_subordinate_to', 'instances', 'records')

# Team
class TeamModelSerializer(serializers.ModelSerializer):
  club = serializers.PrimaryKeyRelatedField(read_only=True)
  is_superset_of = serializers.PrimaryKeyRelatedField(queryset=TeamModel.objects.all())
  is_subset_of = serializers.PrimaryKeyRelatedField(queryset=TeamModel.objects.all())

  class Meta:
    model = TeamModel
    fields = ('_id', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'club', 'is_superset_of', 'is_subset_of')

class TeamInstanceSerializer(serializers.ModelSerializer):
  team = serializers.PrimaryKeyRelatedField(read_only=True)
  event = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = TeamInstance
    fields = ('_id', 'date_created', 'team', 'event')

class TeamRecordSerializer(serializers.ModelSerializer):
  team = serializers.PrimaryKeyRelatedField(read_only=True)
  event = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = TeamRecord
    fields = ('_id', 'date_created', 'team', 'event')

class TeamSerializer(serializers.ModelSerializer):
  model = serializers.PrimaryKeyRelatedField(read_only=True)
  is_superset_of = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
  is_subset_of = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
  instances = TeamInstanceSerializer(many=True)
  records = TeamRecordSerializer(many=True)
  assets = AssetInstanceSerializer(many=True)
  roles = RoleSerializer(many=True)

  class Meta:
    model = Team
    fields = ('_id', 'date_created', 'name', 'club', 'model', 'is_superset_of', 'is_subset_of', 'instances', 'records', 'assets', 'roles')

# Event
class EventModelSerializer(serializers.ModelSerializer):
  club = serializers.PrimaryKeyRelatedField(read_only=True)
  parts = serializers.PrimaryKeyRelatedField(queryset=EventModel.objects.all())
  is_part_of = serializers.PrimaryKeyRelatedField(queryset=EventModel.objects.all())

  class Meta:
    model = EventModel
    fields = ('_id', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'club', 'parts', 'is_part_of')

class EventInstanceSerializer(serializers.ModelSerializer):
  event = serializers.PrimaryKeyRelatedField(read_only=True)
  teams = TeamInstanceSerializer(many=True)

  class Meta:
    model = EventInstance
    fields = ('_id', 'date_created', 'description', 'event', 'teams')

class EventSerializer(serializers.ModelSerializer):

  model = serializers.PrimaryKeyRelatedField(read_only=True)
  parts = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
  is_part_of = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
  instances = EventInstanceSerializer(many=True)

  class Meta:
    model = Event
    fields = ('_id', 'date_created', 'name', 'description', 'model', 'parts', 'is_part_of', 'instances')

# Club
class ClubSerializer(serializers.ModelSerializer):
  asset_models = AssetModelSerializer(many=True)
  role_models = RoleModelSerializer(many=True)
  team_models = TeamModelSerializer(many=True)
  event_models = EventModelSerializer(many=True)

  class Meta:
    model = Club
    fields = ('name', 'asset_models', 'role_models', 'team_models', 'event_models')

# Member
class MemberSerializer(serializers.ModelSerializer):
  roles = RoleSerializer(many=True)

  class Meta:
    model = Member
    fields = ('_id', 'date_created', 'username', 'email', 'first_name', 'last_name', 'is_activated', 'is_enabled', 'is_staff', 'roles')
