
from util.merge import merge
from util.force_array import force_array

from .response import Response
from .errors import errors
from .types import types

class Schema():

  def __init__(self, description=None, server_types=None, children=None):
    self.description = description
    self.server_types = force_array(server_types or types.STRUCTURE())
    self.children = children

  def query(self, payload):
    return None

  def respond(self, payload):

    response = Response(
      description=self.description,
      server_types=self.server_types,
    )

    validated_type = self.validate_server_type(payload)
    if not validated_type:
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
      response.add_child(child_key, child.respond(child_payload))

    return response

  def validate_server_type(self, payload):
    for server_type in self.server_types:
      if server_type.validate(payload):
        self.active_server_type = server_type
        return True
