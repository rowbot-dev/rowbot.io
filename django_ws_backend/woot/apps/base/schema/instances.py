
from util.api import (
  Schema, StructureSchema, IndexedSchema,
  StructureResponse, IndexedResponse,
  types,
  errors,
  constants,
)

from .constants import model_schema_constants

class InstanceSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      children={
        model_schema_constants.ATTRIBUTES: Model.objects.schema_instance_attributes(),
        model_schema_constants.RELATIONSHIPS: Model.objects.schema_instance_relationships(),
      },
    )

  def response_from_model_instance(self, instance, attributes, relationships):
    return self.respond(
      self.model.objects.serialize(
        instance,
        attributes=attributes,
        relationships=relationships,
      )
    )

class InstancesResponse(IndexedResponse):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)

  def add_instances(self, instances, attributes, relationships):
    for instance in instances:
      self.add_child(
        instance._id,
        self.template_schema.response_from_model_instance(
          instance,
          attributes,
          relationships,
        )
      )

class InstancesSchema(IndexedSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(
      **kwargs,
      closed=True,
      response=InstancesResponse,
      template=InstanceSchema(Model),
    )
