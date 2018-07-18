
import json

from django.test import TestCase

from ..api import api
from ..models import Member, Role, RoleModel, Club

class APITestCase(TestCase):
  def setUp(self):
    member1 = Member.objects.create(username='alfred', email='alfred@alfred.com')
    member2 = Member.objects.create(username='alfred1', email='alfred111@alfred.com')
    member3 = Member.objects.create(username='wilbur', email='wilbur@wilbur.com')
    member4 = Member.objects.create(username='jamal', email='aldjamal@wilbur.com')

    club = Club.objects.create(name='club_name')
    role_model = RoleModel.objects.create(club=club)
    Role.objects.create(model=role_model, member=member1, nickname='alfie')
    Role.objects.create(model=role_model, member=member2, nickname='alf')
    Role.objects.create(model=role_model, member=member3, nickname='wil')
    Role.objects.create(model=role_model, member=member4, nickname='jamal')

  def test_empty(self):
    # print(json.dumps(api.respond().render(), indent=2))
    self.assertTrue(True)
    # self.assertTrue(False)

  def test_respond(self):
    payload = {
      'models': {
        'Member': {
          'methods': {
            'filter': {
              'composite': [
                {
                  'key': 'username__contains',
                  'value': 'a',
                },
                {
                  'and': [
                    {
                      'key': 'email__contains',
                      'value': 'd',
                    },
                    {
                      'key': 'email__startswith',
                      'value': 'al',
                    },
                  ],
                },
              ],
            },
          },
        },
      },
    }

    response = api.respond(payload)

    print(json.dumps(response.render(), indent=2))

    self.assertTrue(False)
    # self.assertTrue(True)

  def test_respond_role(self):
    payload = {
      'models': {
        'Role': {
          'attributes': {
            'nickname': True,
            'is_confirmed': True,
          },
          'relationships': None,
          'methods': {
            'filter': {
              'composite': [
                {
                  'key': 'member__username__contains',
                  'value': 'a',
                },
              ],
            },
          },
        },
      },
    }

    response = api.respond(payload)

    print(json.dumps(response.render(), indent=2))

    # self.assertTrue(False)
    self.assertTrue(True)
