
from util.construct_filter_query import construct_filter_query
from util.api import Schema, types, errors, constants

from .constants import model_schema_constants

class FilterSchema(Schema):
  def __init__(self, Model, authorization=None, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description='',
      children={
        model_schema_constants.COMPOSITE: Schema(
          description='',
          server_types=types.STRING(),
        ),
        model_schema_constants.COMPONENTS: Schema(
          description='',
          template=Schema(
            description='',
            children={
              model_schema_constants.KEY: Schema(
                description='',
                server_types=types.STRING(),
              ),
              model_schema_constants.VALUE: Schema(
                description='',
                server_types=types.STRING(),
              ),
            },
          ),
        ),
        model_schema_constants.SORT: Schema(),
        model_schema_constants.PAGINATE: Schema(),
      },
    )

  def consolidate_child_responses(self, child_responses):
    composite = child_responses.get(model_schema_constants.COMPOSITE)
    components = child_responses.get(model_schema_constants.COMPONENTS)

    filter_query, composite_errors, components_errors = construct_filter_query(
      composite=composite,
      components=components,
    )

    composite.errors.extend(composite_errors)
    components.errors.extend(components_errors)

    child_responses.update({
      model_schema_constants.COMPOSITE: composite,
      model_schema_constants.COMPONENTS: components,
    })

    return {
      child_key: child_response
      for child_key, child_response in child_responses.items()
      if child_response.errors
    }

class ModelMethodsSchema(Schema):
  def __init__(self, Model, authorization=None, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description='No available model methods',
      children={
        model_schema_constants.FILTER: FilterSchema(Model, authorization=authorization),
      },
    )
