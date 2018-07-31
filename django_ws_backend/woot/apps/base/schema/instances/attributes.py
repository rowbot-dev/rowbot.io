
from util.api import Schema, StructureSchema, StructureResponse, map_type

class InstanceAttributeResponse(StructureResponse):
  pass

class InstanceAttributeSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=InstanceAttributeResponse,
      description='No available instance methods',
      children={
        attribute_field.name: Schema(
          types=map_type(attribute_field.get_internal_type())
        )
        for attribute_field
        in self.model.objects.attributes()
      },
    )
