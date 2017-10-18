
# DRF
from rest_framework import serializers

# Local
from row.models.asset import AssetCategory, AssetType, Asset, AssetInstance
from row.models.club import Club
from row.models.event import EventCategory, EventType, Event, EventInstance
from row.models.member import Member
from row.models.role import RoleCategory, RoleType, Role, RoleInstance, RoleRecord
from row.models.team import TeamCategory, TeamType, Team, TeamInstance, TeamRecord

# Heirarchy:
# Asset
# Role
# Team
# Event
# Club
# Member

# Asset
class AssetTypeSerializer(serializers.ModelSerializer):
  category = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = AssetType
    fields = ('_id', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'category')

class AssetCategorySerializer(serializers.ModelSerializer):
  types = AssetTypeSerializer(many=True)

  class Meta:
    model = AssetCategory
    fields = ('_id', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'types')

class AssetInstanceSerializer(serializers.ModelSerializer):
  asset = serializers.PrimaryKeyRelatedField(read_only=True)
  team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
  in_possession_of = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

  class Meta:
    model = AssetInstance
    fields = ('_id', 'date_created', 'metadata', 'asset', 'team', 'in_possession_of')

class AssetSerializer(serializers.ModelSerializer):
  club = serializers.PrimaryKeyRelatedField(read_only=True)
  type = serializers.PrimaryKeyRelatedField(read_only=True)
  instances = AssetInstanceSerializer(many=True)

  class Meta:
    model = Asset
    fields = ('_id', 'date_created', 'name', 'location', 'description', 'club', 'type', 'instances')

# Role
class RoleTypeSerializer(serializers.ModelSerializer):
  category = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = RoleType
    fields = ('_id', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'category')

class RoleCategorySerializer(serializers.ModelSerializer):
  types = RoleTypeSerializer(many=True)

  class Meta:
    model = RoleCategory
    fields = ('_id', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'types')

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
  club = serializers.PrimaryKeyRelatedField(read_only=True)
  team = serializers.PrimaryKeyRelatedField(read_only=True)
  type = serializers.PrimaryKeyRelatedField(read_only=True)
  member = serializers.PrimaryKeyRelatedField(read_only=True)
  instances = RoleInstanceSerializer(many=True)
  records = RoleCategorySerializer(many=True)

  class Meta:
    model = Role
    fields = ('_id', 'date_created', 'nickname', 'club', 'team', 'type', 'member', 'instances', 'records')

# Team
class TeamTypeSerializer(serializers.ModelSerializer):
  category = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = TeamType
    fields = ('_id', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'category')

class TeamCategorySerializer(serializers.ModelSerializer):
  types = TeamTypeSerializer(many=True)

  class Meta:
    model = TeamCategory
    fields = ('_id', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'types')

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
  club = serializers.PrimaryKeyRelatedField(read_only=True)
  type = serializers.PrimaryKeyRelatedField(read_only=True)
  instances = TeamInstanceSerializer(many=True)
  records = TeamRecordSerializer(many=True)
  assets = AssetInstanceSerializer(many=True)
  roles = RoleSerializer(many=True)

  class Meta:
    model = Team
    fields = ('_id', 'date_created', 'name', 'club', 'type', 'instances', 'records', 'assets', 'roles')

# Event
class EventTypeSerializer(serializers.ModelSerializer):
  category = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = EventType
    fields = ('_id', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'category')

class EventCategorySerializer(serializers.ModelSerializer):
  types = EventTypeSerializer(many=True)

  class Meta:
    model = EventCategory
    fields = ('_id', 'date_created', 'reference', 'verbose_name', 'verbose_name_plural', 'description', 'types')

class EventInstanceSerializer(serializers.ModelSerializer):
  event = serializers.PrimaryKeyRelatedField(read_only=True)
  teams = TeamInstanceSerializer(many=True)

  class Meta:
    model = EventInstance
    fields = ('_id', 'date_created', 'description', 'event', 'teams')

class EventSerializer(serializers.ModelSerializer):
  club = serializers.PrimaryKeyRelatedField(read_only=True)
  type = serializers.PrimaryKeyRelatedField(read_only=True)
  instances = EventInstanceSerializer(many=True)

  class Meta:
    model = Event
    fields = ('_id', 'date_created', 'name', 'description', 'club', 'type', 'instances')

# Club
class ClubSerializer(serializers.ModelSerializer):
  assets = AssetSerializer(many=True)
  roles = RoleSerializer(many=True)
  teams = TeamSerializer(many=True)
  events = EventSerializer(many=True)

  class Meta:
    model = Club
    fields = ('name', 'assets', 'roles', 'teams', 'events')

# Member
class MemberSerializer(serializers.ModelSerializer):
  roles = RoleSerializer(many=True)

  class Meta:
    model = Member
    fields = ('_id', 'date_created', 'username', 'email', 'first_name', 'last_name', 'is_activated', 'is_enabled', 'is_staff', 'roles')
