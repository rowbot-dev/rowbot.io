
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

    self.children.update({
      model_schema_constants.REFERENCE: reference_group_model.objects.schema(),
    })

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

    models_in_payload = self.active_response.children.keys() - set(model_schema_constants.REFERENCE)

    if models_in_payload:
      for model_name in models_in_payload:
        model_response = self.active_response.get_child(model_name)
        methods_response = model_response.get_child(model_schema_constants.METHODS)

        if methods_response is not None:
          for method_response in methods_response.children.values():
            for external_queryset in method_response.external_querysets:
              external_model_name = external_queryset.model.__name__
              external_model_response = self.active_response.force_get_child(external_model_name)
              external_model_instances_response = external_model_response.force_get_child(model_schema_constants.INSTANCES)
              external_model_instances_response.add_instances(external_queryset)

            if method_response.reference is not None:
              reference_instance = self.reference_group_model.objects.get(id=method_response.reference)
              reference_response = self.active_response.force_get_child(model_schema_constants.REFERENCE)
              reference_instances_response = reference_response.force_get_child(model_schema_constants.INSTANCES)
              reference_instances_response.add_instances([reference_instance])

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

    methods_response = self.active_response.get_child(model_schema_constants.METHODS)

    if methods_response is not None:
      attributes_response = self.active_response.force_get_child(model_schema_constants.ATTRIBUTES)
      relationships_response = self.active_response.force_get_child(model_schema_constants.RELATIONSHIPS)
      instances_response = self.active_response.force_get_child(model_schema_constants.INSTANCES)

      methods_internal_instances = []
      for methods_child in methods_response.children.values():
        if methods_child.internal_queryset is not None:
          methods_internal_instances.extend(list(methods_child.internal_queryset))

      instances_response.add_attributes(attributes_response.get_attributes())
      instances_response.add_relationships(relationships_response.get_relationships())
      instances_response.add_instances(methods_internal_instances)

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
