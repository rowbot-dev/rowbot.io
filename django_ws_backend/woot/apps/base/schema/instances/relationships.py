
from util.api import Schema, StructureSchema, StructureResponse, types

class InstanceRelationshipResponse(StructureResponse):
  pass

class InstanceRelationshipSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=InstanceRelationshipResponse,
      description='No available instance methods',
      children={
        relationship_field.name: Schema(
          description='No available instance methods',
          types=[
            types.REF(),
            types.ARRAY(),
            types.NULL(),
          ],
        )
        for relationship_field
        in self.model.objects.relationships()
      }
    )
