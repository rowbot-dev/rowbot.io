
from util.merge import merge
from util.api import StructureSchema, types, errors, constants

from .constants import model_schema_constants
from .attributes import AttributeSchema
from .relationships import RelationshipSchema
from .instances import InstancesSchema
from .methods import ModelMethodsSchema

class ModelSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      model_schema_constants.ATTRIBUTES: Model.objects.schema_attributes(),
      model_schema_constants.METHODS: Model.objects.schema_model_methods(),
      # model_schema_constants.RELATIONSHIPS: Model.objects.schema_relationships(),
      model_schema_constants.INSTANCES: Model.objects.schema_instances(),
    }

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

    attributes_response = self.active_response.children.get(model_schema_constants.ATTRIBUTES)
    methods_response = self.active_response.children.get(model_schema_constants.METHODS)
    instances_response = self.active_response.children.get(model_schema_constants.INSTANCES)

    if methods_response is not None:
      if instances_response is None:
        instances_response = self.children.get(model_schema_constants.INSTANCES).get_response()

      if attributes_response is None:
        attributes_response = self.children.get(model_schema_constants.ATTRIBUTES).get_response()

      methods_internal_instances = []
      for methods_child in methods_response.children.values():
        methods_internal_instances.extend(list(methods_child.internal_queryset))

      instances_response.add_instances(methods_internal_instances, attributes_response.get_attributes())

      self.active_response.children.update({
        model_schema_constants.INSTANCES: instances_response,
      })
