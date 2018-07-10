
from util.api import Schema, StructureSchema, types

class AttributeSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      field.name: Schema(
        description='',
        server_types=types.BOOLEAN(),
      )
      for field in Model._meta.get_fields()
      if (
        not field.is_relation
      )
    }
