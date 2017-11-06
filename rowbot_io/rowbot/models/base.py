
### Django
from django.db import models
from django.db.models import Q

### Local

### Util
import uuid
from uuid import UUID
import string
import random

# random key
def random_key():
  chars = string.ascii_uppercase + string.digits
  return ''.join([random.choice(chars) for _ in range(8)])

def is_valid_uuid(uuid_string):
  try:
    if hasattr(uuid_string, 'hex') and is_valid_uuid(uuid_string.hex):
      val = uuid_string
    else:
      val = UUID(uuid_string, version=4)
  except ValueError:
    return False
  return str(val) == uuid_string or val.hex == uuid_string or val == uuid_string

### Manager
class Manager(models.Manager):
  use_for_related_fields = True
  def get(self, **kwargs):

    # filter first
    if self.filter(**kwargs).exists():
      return super().get(**kwargs)
    return None

### Base
class Model(models.Model):

  objects = Manager()

  class Meta:
    abstract = True

  ### Properties
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  date_created = models.DateTimeField(auto_now_add=True)

  @property
  def _id(self):
    return self.id.hex

  @property
  def _ref(self):
    return '{}.{}'.format(self.__class__.__name__, self._id)
