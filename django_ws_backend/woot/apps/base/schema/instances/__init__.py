
from util.api import (
  Schema, ClosedSchema, StructureSchema, IndexedSchema,
  StructureResponse, IndexedResponse,
  types,
  errors,
  constants,
)

from ..constants import model_schema_constants
from .attributes import InstanceAttributeSchema
from .relationships import InstanceRelationshipSchema

class InstanceResponse(StructureResponse):
  def render_value(self):
    self.rendered = {
      child_key: child_response.render()
      for child_key, child_response in self.children.items()
      if child_response.children
    }

class InstanceSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=InstanceResponse,
      children={
        model_schema_constants.ATTRIBUTES: Model.objects.schema_instance_attributes(),
        model_schema_constants.RELATIONSHIPS: Model.objects.schema_instance_relationships(),
      },
    )

  def response_from_model_instance(self, instance, attributes=None, relationships=None):
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
    self.attributes = None
    self.relationships = None

  def add_attributes(self, attributes):
    self.attributes = attributes

  def add_relationships(self, relationships):
    self.relationships = relationships

  def add_instances(self, instances):
    for instance in instances:
      self.add_child(
        instance._id,
        self.template_schema.response_from_model_instance(
          instance,
          attributes=self.attributes,
          relationships=self.relationships,
        )
      )

class InstancesSchema(IndexedSchema, ClosedSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(
      **kwargs,
      response=InstancesResponse,
      template=InstanceSchema(Model),
    )
