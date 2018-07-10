
from util.merge import merge
from util.force_array import force_array

from .response import Response, StructureResponse, ArrayResponse, IndexedResponse, TemplateResponse
from .errors import errors
from .types import types
from .constants import constants

class Schema():
  default_server_types = types.STRING()

  def __init__(self, description=None, server_types=None):
    self.description = description
    self.server_types = force_array(server_types or self.default_server_types)

  def response(self):
    return Response(description=self.description, server_types=self.server_types)

  def respond(self, payload=None):
    self.active_response = self.response()

    if payload is None:
      self.responds_to_none()
      return self.active_response

    if not self.passes_type_validation(payload):
      return self.active_response

    if not self.passes_pre_response_checks(payload):
      return self.active_response

    self.responds_to_valid_payload(payload)
    return self.active_response

  def responds_to_none(self):
    self.active_response.is_empty = True

  def passes_type_validation(self, payload):
    for server_type in self.server_types:
      if server_type.validate(payload):
        self.active_response.active_server_type = server_type
        return True

    self.active_response.add_error(errors.SERVER_TYPES(self.server_types))
    return False

  def passes_pre_response_checks(self, payload):
    return True

  def responds_to_valid_payload(self, payload):
    self.active_response.add_value(payload)

class StructureSchema(Schema):
  default_server_types = types.STRUCTURE()

  def __init__(self, **kwargs, children=None):
    super().__init__(**kwargs)
    self.children = children

  def response(self):
    return StructureResponse(description=self.description, server_types=self.server_types)

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
  default_server_types = types.ARRAY()

  def __init__(self, template=None, **kwargs):
    super().__init__(**kwargs)
    self.template = template

  def response(self):
    return ArrayResponse(
      description=self.description,
      server_types=self.server_types,
      template=self.template,
    )

  def responds_to_valid_payload(self, payload):
    for child_payload in payload:
      self.active_response.add_child(self.template.respond(child_payload))

class IndexedSchema(Schema):
  default_server_types = types.STRUCTURE()
  default_index_type = types.UUID()

  def __init__(self, index_type=None, template=None, **kwargs):
    super().__init__(**kwargs)
    self.index_type = index_type or self.default_index_type
    self.template = template

  def response(self):
    return IndexedResponse(
      description=self.description,
      server_types=self.server_types,
      template=self.template,
    )

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
      self.active_response.add_error(errors.INVALID_INDEXES(invalid_indexes, self.index_type))
      return False

    return True

  def responds_to_valid_payload(self, payload):
    for child_index, child_payload in payload.items():
      self.active_response.add_child(child_index, self.template.respond(child_payload))

class TemplateSchema(Schema):
  default_server_types = types.STRUCTURE()

  def __init__(self, template=None, **kwargs):
    super().__init__(**kwargs)
    self.template = template

  def response(self):
    return TemplateResponse(
      description=self.description,
      server_types=self.server_types,
      template=self.template,
    )

  def responds_to_valid_payload(self, payload):
    self.responds_to_none()
