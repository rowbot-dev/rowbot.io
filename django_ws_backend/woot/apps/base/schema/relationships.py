
from util.api import Schema, StructureSchema, StructureResponse, Error, types

class UniformRelationshipInclusiveError(Error):
  def __init__(self):
    return super().__init__(
      code='125',
      name='uniform_relationship_inclusive',
      description='Relationship keys must be all inclusive or exclusive',
    )

class RelationshipResponse(StructureResponse):
  def __init__(self, parent_schema):
    self.is_inclusive = False
    super().__init__(parent_schema)

  def get_relationships(self):
    relationship_names = {
      field.name
      for field in self.parent_schema.model.objects.relationships()
    }
    child_keys = self.children.keys()

    if not child_keys:
      return list(relationship_names)

    if self.is_inclusive:
      return list(child_keys)

    return list(relationship_names - child_keys)

class RelationshipSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=RelationshipResponse,
      children={
        relationship.name: Schema(
          description='',
          server_types=types.BOOLEAN(),
        )
        for relationship in Model.objects.relationships()
      },
    )

  def passes_pre_response_checks(self, payload):
    passes_pre_response_checks = super().passes_pre_response_checks(payload)

    values = payload.values()
    if any(values) and not all(values):
      self.active_response.add_error(UniformRelationshipInclusiveError())
      return False

    if all(values):
      self.active_response.is_inclusive = True

    return passes_pre_response_checks
