
from django.test import TestCase
from util.merge import merge
from apps.rowbot.models.member import Member

class MemberSchemaTestCase(TestCase):
  def test_member_schema(self):
    schema = Member.objects.schema()

    self.assertEqual(
      schema,
      {
        'attributes': {
          'activation_email_key': 'CharField',
          'activation_email_sent': 'BooleanField',
          'activation_key': 'UUIDField',
          'date_created': 'DateTimeField',
          'email': 'CharField',
          'first_name': 'CharField',
          'id': 'UUIDField',
          'is_activated': 'BooleanField',
          'is_enabled': 'BooleanField',
          'is_staff': 'BooleanField',
          'is_superuser': 'BooleanField',
          'last_login': 'DateTimeField',
          'last_name': 'CharField',
          'password': 'CharField',
          'username': 'CharField'
        },
        'relationships': {
          'groups': 'Group',
          'logentry': 'LogEntry',
          'roles': 'Role',
          'tokens': 'AuthenticationToken',
          'user_permissions': 'Permission'
        },
        'methods': {
          'activate': {
            'activation_key': 'string',
          },
          'send_activation_email': {},
        },
      },
    )
