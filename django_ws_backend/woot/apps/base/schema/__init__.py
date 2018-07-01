
from util.merge import merge
from util.api import Schema, types, errors, constants

from .constants import model_schema_constants
from .attributes import AttributeSchema
from .relationships import RelationshipSchema
from .instances import InstancesSchema
from .methods import ModelMethodsSchema

class ModelSchema(Schema):
  def __init__(self, Model, authorization=None, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      model_schema_constants.ATTRIBUTES: Model.objects.schema_attributes(),
      model_schema_constants.RELATIONSHIPS: Model.objects.schema_relationships(),
      model_schema_constants.INSTANCES: Model.objects.schema_instances(),
      model_schema_constants.METHODS: Model.objects.schema_model_methods(),
      # model_schema_constants.FILTER: FilterSchema(Model, authorization=authorization),
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

  def query(self, payload):
    pass
