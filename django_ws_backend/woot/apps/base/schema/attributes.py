
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
    super().__init__(parent_schema)

  def get_attributes(self):
    attribute_names = {
      field.name
      for field in self.parent_schema.model.objects.attributes()
    }
    child_keys = self.children.keys()

    if not child_keys:
      return list(attribute_names)

    if self.is_inclusive:
      return list(child_keys)

    return list(attribute_names - child_keys)

class AttributeSchema(StructureSchema):
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
    passes_pre_response_checks = super().passes_pre_response_checks(payload)

    values = payload.values()
    if any(values) and not all(values):
      self.active_response.add_error(UniformAttributeInclusiveError())
      return False

    if all(values):
      self.active_response.is_inclusive = True

    return passes_pre_response_checks
