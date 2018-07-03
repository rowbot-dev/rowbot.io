
import re

from django.db.models import Q

from util.api.errors import Error
from util.random_string import random_string

class CompositeComponentsXNORFailedError(Error):
  pass

class CompositeKeyNotFoundInComponentsError(Error):
  pass

class CompositeInvalidTokenParseError(Error):
  pass

class CompositeInvalidCharacterError(Error):
  pass

class ComponentsInvalidQueryError(Error):
  pass

def construct_filter_query(composite=None, components=None, sorting=None, pagination=None):
  return None, []
