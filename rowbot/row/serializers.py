
# DRF
from rest_framework import serializers

# Local
from row.models.member import Member

# Member
class MemberSerializer(serializers.ModelSerializer):
  class Meta:
    model = Member
    fields = ('_id', 'username', 'email', 'first_name', 'last_name', 'is_activated', 'is_enabled', 'is_staff')
