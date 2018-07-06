
from util.api import Schema, StructureSchema, TemplateSchema, types, errors, constants

from .constants import model_schema_constants

class SingleInstanceSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      model_schema_constants.ATTRIBUTES: TemplateSchema(
        description='Get and set attributes of the instance',
        template=StructureSchema(
          description=(
            'A list of attributes can be found in the attribute '
            'portion of the model schema. The structure here shows '
            'how to interact with a single attribute'
          ),
          server_types=[
            types.BOOLEAN('A value of true will be assumed to be a get request'),
            types.STRUCTURE('Control get and set behaviour'),
          ],
          children={
            model_schema_constants.GET: Schema(
              description='Interface to refresh the local value of an attribute',
              server_types=types.BOOLEAN('A value of true will update the attribute from the system'),
            ),
            model_schema_constants.SET: Schema(
              description='Interface to set the remote value of the attribute',
              server_types=types.ANY('Any value will be typechecked against the type specified in the attribute schema'),
            ),
          },
        ),
      ),
      model_schema_constants.RELATIONSHIPS: TemplateSchema(
        description='Get and set relationships of the instance',
        template=StructureSchema(
          description=(
            'A list of relationships can be found in the relationship '
            'portion of the model schema. The structure here shows '
            'how to interact with a single relationship'
          ),
          server_types=[
            types.BOOLEAN('A value of true will be assumed to be a get request'),
            types.STRUCTURE('Control get and set behaviour'),
          ],
          children={
            model_schema_constants.GET: Schema(
              description='Interface to refresh to local value of an relationship',
              server_types=types.BOOLEAN('A value of true will update the attribute from the system'),
            ),
            model_schema_constants.SET: Schema(
              description='Interface to set the remote value of the attribute',
              server_types=types.ANY('Any value will be typechecked against the type specified in the attribute schema'),
            ),
          },
        ),
      ),
      model_schema_constants.METHODS: Model.objects.schema_instance_methods(),
    }

class InstancesSchema(TemplateSchema):
  def __init__(self, Model, authorization=None, **kwargs):
    super().__init__(**kwargs)
    self.template = SingleInstanceSchema(Model)

  def query(self, payload):
    pass
