
from util.merge import merge
from util.api import Schema, StructureSchema, types, errors, Error, constants

from .constants import model_schema_constants
from .attributes import AttributeSchema
from .relationships import RelationshipSchema
from .instances import InstancesSchema
from .methods import ModelMethodsSchema

class ModelsSchemaWithReferences(StructureSchema):
  def __init__(self, reference_group_model=None, **kwargs):
    self.reference_group_model = reference_group_model
    super().__init__(**kwargs)
    for child in self.children.values():
      child.add_reference_group_model(reference_group_model)

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

    for child_response_key, child_response in self.active_response.children.items():
      print(child_response_key, child_response.children.get(model_schema_constants.INSTANCES))

class ModelSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      model_schema_constants.ATTRIBUTES: Model.objects.schema_attributes(),
      model_schema_constants.RELATIONSHIPS: Model.objects.schema_relationships(),
      model_schema_constants.METHODS: Model.objects.schema_model_methods(),
      model_schema_constants.INSTANCES: Model.objects.schema_instances(),
    }

  def add_reference_group_model(self, reference_group_model):
    self.reference_group_model = reference_group_model
    methods_schema = self.children.get(model_schema_constants.METHODS)
    methods_schema.add_reference_group_model(reference_group_model)

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

    attributes_response = self.active_response.children.get(model_schema_constants.ATTRIBUTES)
    relationships_response = self.active_response.children.get(model_schema_constants.RELATIONSHIPS)
    methods_response = self.active_response.children.get(model_schema_constants.METHODS)
    instances_response = self.active_response.children.get(model_schema_constants.INSTANCES)

    if methods_response is not None:
      if instances_response is None:
        instances_response = self.children.get(model_schema_constants.INSTANCES).get_response()

      if attributes_response is None:
        attributes_response = self.children.get(model_schema_constants.ATTRIBUTES).get_response()

      if relationships_response is None:
        relationships_response = self.children.get(model_schema_constants.RELATIONSHIPS).get_response()

      methods_internal_instances = []
      for methods_child in methods_response.children.values():
        if methods_child.internal_queryset is not None:
          methods_internal_instances.extend(list(methods_child.internal_queryset))

      instances_response.add_instances(
        methods_internal_instances,
        attributes_response.get_attributes(),
        relationships_response.get_relationships(),
      )

      self.active_response.children.update({
        model_schema_constants.INSTANCES: instances_response,
      })

class SchemaManagerMixin:
  def schema(self):
    return ModelSchema(self.model)

  def schema_attributes(self, authorization=None):
    return AttributeSchema(self.model)

  def schema_relationships(self, authorization=None):
    return RelationshipSchema(self.model)

  def schema_model_methods(self):
    return ModelMethodsSchema(self.model)

  def schema_instance_attributes(self):
    return StructureSchema(
      description='No available instance methods',
      children={
        attribute_field.name: Schema()
        for attribute_field
        in self.attributes()
      }
    )

  def schema_instance_relationships(self):
    return StructureSchema(
      description='No available instance methods',
      children={
        relationship_field.name: Schema(
          description='No available instance methods',
          server_types=[
            types.REF(),
            types.ARRAY(),
            types.NULL(),
          ],
        )
        for relationship_field
        in self.relationships()
      }
    )

  def schema_instance_methods(self):
    return Schema(description='No available instance methods')

  def schema_instances(self):
    return InstancesSchema(self.model)
