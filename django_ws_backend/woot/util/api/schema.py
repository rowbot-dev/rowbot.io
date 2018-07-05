
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
    self.active_response = None

  def query(self, payload=None):
    return payload

  def response(self):
    return Response(
      description=self.description,
      server_types=self.server_types,
    )

  def respond(self, payload=None):
    self.active_response = self.response()

    if payload is None:
      self.active_response.empty = True

      if self.template is not None:
        self.active_response.template = self.template.respond()

      if self.children is not None:
        for child_key, child in self.children.items():
          self.active_response.add_child(child_key, child.respond())

      return self.active_response

    if not self.validate_server_type(payload):
      return self.active_response.add_error(errors.SERVER_TYPES(self.server_types))

    if not self.children:
      if self.template:
        return self.active_response.add_value(self.template_responses(payload))

      return self.active_response.add_value(self.query(payload))

    invalid_keys = payload.keys() - self.children.keys()
    if invalid_keys:
      return self.active_response.add_error(errors.INVALID_KEYS(invalid_keys))

    child_responses = self.child_responses(payload)

    if child_responses is not None:
      for child_key, child_response in child_responses.items():
        if child_response is not None:
          self.active_response.add_child(child_key, child_response)

    return self.active_response

  def template_responses(self, payload):
    if isinstance(payload, list):
      return self.consolidate_child_responses([
        self.template.respond(payload=child_payload)
        for child_payload in payload
      ])

    return self.consolidate_child_responses({
      child_key: self.template.respond(payload=child_payload)
      for child_key, child_payload in payload.items()
      if child_key in payload
    })

  def child_responses(self, payload):
    return self.consolidate_child_responses({
      child_key: child.respond(payload=payload.get(child_key))
      for child_key, child in self.children.items()
      if child_key in payload
    })

  def consolidate_child_responses(self, child_responses):
    return child_responses

  def validate_server_type(self, payload):
    for server_type in self.server_types:
      if server_type.validate(payload):
        self.active_server_type = server_type
        return True

class DefaultSchema(Schema):
  pass
