
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

  def query(self, payload=None):
    return None

  def response(self):
    return Response(
      description=self.description,
      server_types=self.server_types,
    )

  def respond(self, payload=None):
    response = self.response()

    if payload is None:
      response.empty = True

      if self.template is not None:
        response.template = self.template.respond()

      if self.children is not None:
        for child_key, child in self.children.items():
          response.add_child(child_key, child.respond())

      return response

    if not self.validate_server_type(payload):
      return response.add_error(errors.SERVER_TYPES(self.server_types))

    if not self.children:
      return response.add_value(self.query(payload))

    invalid_keys = payload.keys() - self.children.keys()
    if invalid_keys:
      return response.add_error(errors.INVALID_KEYS(invalid_keys))

    child_responses = self.child_responses(payload)

    for child_key, child_response in child_responses.items():
      if child_response is not None:
        response.add_child(child_key, child_response)

    return response

  def child_responses(self, payload):
    return self.consolidate({
      child_key: child.respond(payload=payload.get(child_key))
      for child_key, child in self.children.items()
      if child_key in payload
    })

  def consolidate(self, child_responses):
    return child_responses

  def validate_server_type(self, payload):
    for server_type in self.server_types:
      if server_type.validate(payload):
        self.active_server_type = server_type
        return True

class DefaultSchema(Schema):
  pass
