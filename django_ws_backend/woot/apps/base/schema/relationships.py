
from util.api import Schema

class RelationshipSchema(Schema):
  def __init__(self, Model, authorization=None, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      field.name: Schema()
      for field in Model._meta.get_fields()
      if field.is_relation
    }

  def query(self, payload):
    pass
