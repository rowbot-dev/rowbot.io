
from util.api import Schema, StructureSchema

class RelationshipSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      field.name: Schema()
      for field in Model._meta.get_fields()
      if field.is_relation
    }
