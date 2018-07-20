
from util.force_array import force_array
from util.api import Schema, StructureSchema, StructureResponse, Error, types

class UniformAttributeInclusiveError(Error):
  def __init__(self):
    return super().__init__(
      code='124',
      name='uniform_attribute_inclusive',
      description='Attribute keys must be all inclusive or exclusive',
    )

class AttributeResponse(StructureResponse):
  def __init__(self, parent_schema):
    self.is_inclusive = False
    self.should_include_attributes = True
    super().__init__(parent_schema)

  def get_attributes(self):
    attribute_names = {
      field.name
      for field in self.parent_schema.model.objects.attributes()
    }
    child_keys = self.children.keys()

    if not self.should_include_attributes:
      self.should_render = False
      return []

    if not child_keys:
      return list(attribute_names)

    if self.is_inclusive:
      return list(child_keys)

    return list(attribute_names - child_keys)

class AttributeSchema(StructureSchema):
  default_server_types = force_array(StructureSchema.default_server_types) + [
    types.BOOLEAN(),
  ]
  available_errors = StructureSchema.available_errors + [
    UniformAttributeInclusiveError(),
  ]

  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=AttributeResponse,
      children={
        attribute.name: Schema(
          description='',
          server_types=types.BOOLEAN(),
        )
        for attribute in Model.objects.attributes()
      },
    )

  def passes_pre_response_checks(self, payload):
    if self.active_response.active_server_type == types.BOOLEAN():
      return True

    passes_pre_response_checks = super().passes_pre_response_checks(payload)

    values = payload.values()
    if any(values) and not all(values):
      self.active_response.add_error(UniformAttributeInclusiveError())
      return False

    if all(values):
      self.active_response.is_inclusive = True

    return passes_pre_response_checks

  def responds_to_valid_payload(self, payload):
    if self.active_response.active_server_type == types.BOOLEAN():
      self.active_response.should_include_attributes = payload
      return

    super().responds_to_valid_payload(payload)
