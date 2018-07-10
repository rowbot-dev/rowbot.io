
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
      model_schema_constants.METHODS: Model.objects.schema_model_methods(),
      model_schema_constants.ATTRIBUTES: Model.objects.schema_attributes(),
      # model_schema_constants.RELATIONSHIPS: Model.objects.schema_relationships(),
      model_schema_constants.INSTANCES: Model.objects.schema_instances(),
    }

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

    methods_response = self.active_response.children.get(model_schema_constants.METHODS)
    attributes_response = self.active_response.children.get(model_schema_constants.ATTRIBUTES)
    instances_response = self.active_response.children.get(model_schema_constants.INSTANCES)

    if methods_response is not None:
      if instances_response is None:
        instances_response = self.children.get(model_schema_constants.INSTANCES).response()

      for method_response in methods_response.children.values():
        instances_response.add_queryset(method_response.internal_queryset)

    if instances_response is not None:
      if attributes_response is not None:
        instances_response.add_attributes(attributes_response.render())

      self.active_response.children.update({model_schema_constants.INSTANCES: instances_response})
