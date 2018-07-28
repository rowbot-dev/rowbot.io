
from util.merge import merge
from util.force_array import force_array

from .response import (
  Response,
  StructureResponse,
  ArrayResponse,
  IndexedResponse,
)
from .errors import errors
from .types import types
from .constants import constants

class Schema():
  default_types = [
    types.STRING(),
  ]
  default_response = Response
  available_errors = [
    errors.TYPES(),
  ]

  def __init__(self, description=None, types=None, response=None, client=None, closed=False):
    self.description = description
    self.types = force_array(types or self.default_types)
    self.response = response or self.default_response
    self.client = client

  def get_response(self):
    return self.response(self)

  def respond(self, payload=None):
    self.active_response = self.get_response()

    if payload is None:
      self.responds_to_none()
      return self.active_response

    if not self.passes_type_validation(payload):
      return self.active_response

    if not self.passes_pre_response_checks(payload):
      return self.active_response

    self.responds_to_valid_payload(payload)

    self.responds_to_client()

    return self.active_response

  def responds_closed(self):
    self.active_response.add_error(errors.CLOSED())

  def responds_to_none(self):
    self.active_response.is_empty = True

  def passes_type_validation(self, payload):
    for type in self.types:
      if type.validate(payload):
        self.active_response.active_type = type
        return True

    self.active_response.add_error(errors.TYPES(types=self.types))
    return False

  def passes_pre_response_checks(self, payload):
    return True

  def responds_to_valid_payload(self, payload):
    self.active_response.add_value(payload)

  def responds_to_client(self):
    if self.client is not None:
      self.active_response = self.client.respond(payload=self.active_response.render())

class ClosedSchema(Schema):
  available_errors = [
    errors.CLOSED(),
  ]

  def respond(self, payload=None):
    self.active_response = self.get_response()

    if payload is not None:
      self.active_response.add_error(errors.CLOSED())
      return self.active_response

    return super().respond(payload=payload)

class StructureSchema(Schema):
  default_types = [
    types.STRUCTURE(),
  ]
  default_response = StructureResponse
  available_errors = Schema.available_errors + [
    errors.INVALID_KEYS(),
  ]

  def __init__(self, children={}, **kwargs):
    super().__init__(**kwargs)
    self.children = children

  def responds_to_none(self):
    super().responds_to_none()
    for child_key, child_schema in self.children.items():
      self.active_response.add_child(child_key, child_schema.respond())

  def passes_pre_response_checks(self, payload):
    invalid_keys = payload.keys() - self.children.keys()
    if invalid_keys:
      for invalid_key in invalid_keys:
        self.active_response.add_error(errors.INVALID_KEYS(invalid_keys))
      return False

    return super().passes_pre_response_checks(payload)

  def responds_to_valid_payload(self, payload):
    for child_key, child_schema in self.children.items():
      if child_key in payload:
        self.active_response.add_child(child_key, child_schema.respond(payload.get(child_key)))

class ArraySchema(Schema):
  default_types = [
    types.ARRAY(),
  ]
  default_response = ArrayResponse

  def __init__(self, template=None, **kwargs):
    super().__init__(**kwargs)
    self.template = template

  def responds_to_valid_payload(self, payload):
    for child_payload in payload:
      self.active_response.add_child(self.template.respond(child_payload))

class IndexedSchema(Schema):
  default_types = [
    types.STRUCTURE(),
  ]
  default_index_type = types.UUID()
  default_response = IndexedResponse
  available_errors = Schema.available_errors + [
    errors.INVALID_INDEXES(),
  ]

  def __init__(self, index_type=None, template=None, **kwargs):
    super().__init__(**kwargs)
    self.index_type = index_type or self.default_index_type
    self.template = template

  def passes_type_validation(self, payload):
    passes_type_validation = super().passes_type_validation(payload)
    if not passes_type_validation:
      return False

    invalid_indexes = [
      index
      for index in payload.keys()
      if not self.index_type.validate(index)
    ]

    if invalid_indexes:
      self.active_response.add_error(errors.INVALID_INDEXES(indexes=invalid_indexes, index_type=self.index_type))
      return False

    return True

  def responds_to_valid_payload(self, payload):
    for child_index, child_payload in payload.items():
      self.active_response.add_child(child_index, self.template.respond(child_payload))
