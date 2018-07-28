
import json

from django.db import models
from django.test import TestCase

from apps.base.models import MockParentModel

from ..get import GetSchema

class DeleteSchemaTestCase(TestCase):
  def setUp(self):
    self.mock_parent = MockParentModel.objects.create(name='mock_parent')
    self.schema = GetSchema(MockParentModel)

  def test_delete(self):
    payload = [
      self.mock_parent._id,
    ]

    response = self.schema.respond(payload)

    print(json.dumps(response.render(), indent=2))

    self.assertTrue(False)
