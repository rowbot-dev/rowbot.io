
from util.merge import merge
from util.api import Schema, types, map_type, errors, constants

class model_schema_constants:
  ATTRIBUTES = '_attributes'
  RELATIONSHIPS = '_relationships'
  METHODS = '_methods'
  INSTANCES = '_instances'
  FILTER = '_filter'
  SORT = '_sort'
  PAGINATE = '_paginate'
  CREATE = '_create'
  DELETE = '_delete'
  ARGUMENTS = '_arguments'
  GET = '_get'
  SET = '_set'

class AttributeSchema(Schema):
  def __init__(self, Model, authorization=None, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      field.name: Schema(
        description='',
        server_types=map_type(field.get_internal_type())
      )
      for field in Model._meta.get_fields()
      if (
        not field.is_relation
      )
    }

  def query(self, payload):
    pass

class RelationshipSchema(Schema):
  def __init__(self, Model, authorization=None, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      field.name: Schema()
      for field in Model._meta.get_fields()
      if field.is_relation
    }

  def query(self, payload):
    pass

class SingleInstanceSchema(Schema):
  def __init__(self, Model, authorization=None, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      model_schema_constants.ATTRIBUTES: Schema(
        description='Get and set attributes of the instance',
        template=Schema(
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
              description='Interface to refresh to local value of an attribute',
              server_types=types.BOOLEAN('A value of true will update the attribute from the system'),
            ),
            model_schema_constants.SET: Schema(
              description='Interface to set the remote value of the attribute',
              server_types=types.ANY('Any value will be typechecked against the type specified in the attribute schema'),
            ),
          },
        ),
      ),
      model_schema_constants.RELATIONSHIPS: Schema(
        description='Get and set relationships of the instance',
        template=Schema(
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
      model_schema_constants.METHODS: Model.objects.schema_instance_methods(authorization=authorization),
    }

class InstancesSchema(Schema):
  def __init__(self, Model, authorization=None, **kwargs):
    super().__init__(**kwargs)
    self.template = SingleInstanceSchema(Model, authorization=authorization)

  def query(self, payload):
    pass

class FilterSchema(Schema):
  def __init__(self, Model, authorization=None, **kwargs):
    super().__init__(**kwargs)
    self.model = Model

  def query(self, payload):
    print(payload)

class ModelSchema(Schema):
  def __init__(self, Model, authorization=None, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      model_schema_constants.ATTRIBUTES: Model.objects.schema_attributes(),
      model_schema_constants.RELATIONSHIPS: Model.objects.schema_relationships(),
      model_schema_constants.INSTANCES: Model.objects.schema_instances(),
      model_schema_constants.METHODS: Model.objects.schema_model_methods(),
      model_schema_constants.FILTER: FilterSchema(Model, authorization=authorization),
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
