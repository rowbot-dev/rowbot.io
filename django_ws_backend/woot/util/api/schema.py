
from util.merge import merge
from util.force_array import force_array

from .response import Response
from .errors import errors
from .types import types
from .constants import constants

class Schema():
  default_server_types = types.STRUCTURE('Fine control of content')

  def __init__(self, description=None, server_types=None, template=None, children=None):
    self.description = description
    self.server_types = force_array(server_types or self.default_server_types)
    self.children = children
    self.template = template
    self.active_server_type = None

  def query(self, payload):
    return None

  def respond(self, payload):

    response = Response(
      description=self.description,
      server_types=self.server_types,
    )

    type_validated = self.validate_server_type(payload)
    if not type_validated:
      response.add_error(errors.SERVER_TYPES(self.server_types))
      return response

    if not self.children:
      response.add_value(self.query(payload))
      return response

    unrecognised_keys = payload.keys() - self.children.keys()
    if unrecognised_keys:
      response.add_error(errors.UNRECOGNISED_KEYS(unrecognised_keys))
      return response

    for child_key, child in self.children.items():
      child_payload = payload.get(child_key)
      if child_payload is not None and child is not None:
        response.add_child(child_key, child.respond(child_payload))

    return response

  def empty(self):

    response = Response(
      description=self.description,
      server_types=self.server_types,
    )

    if self.template:
      response.template = self.template.empty()

    if self.children:
      for child_key, child in self.children.items():
        if child is not None:
          response.add_child(child_key, child.empty())

    return response

  def validate_server_type(self, payload):
    for server_type in self.server_types:
      if server_type.validate(payload):
        self.active_server_type = server_type
        return True

class DefaultSchema(Schema):
  pass
