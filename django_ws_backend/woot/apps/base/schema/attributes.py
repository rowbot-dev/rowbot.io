
from util.api import Schema, StructureSchema, types, map_type

class AttributeSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      field.name: Schema(
        description='',
        server_types=map_type(field.get_internal_type())
      )
      for field in Model._meta.get_fields()
      if (
        not field.is_relation
      )
    }
