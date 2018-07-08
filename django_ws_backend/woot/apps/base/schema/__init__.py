
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
      # model_schema_constants.ATTRIBUTES: Model.objects.schema_attributes(),
      # model_schema_constants.RELATIONSHIPS: Model.objects.schema_relationships(),
      # model_schema_constants.INSTANCES: Model.objects.schema_instances(),
      model_schema_constants.METHODS: Model.objects.schema_model_methods(),
      # model_schema_constants.SORT: Schema(
      #   description='',
      # ),
      # model_schema_constants.PAGINATE: Schema(
      #   description='',
      # ),
      # model_schema_constants.CREATE: Schema(
      #   description='',
      # ),
      # model_schema_constants.DELETE: Schema(
      #   description='',
      # ),
    }
