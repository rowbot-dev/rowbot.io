
from util.construct_filter_query import construct_filter_query
from util.api import Schema, types, errors, constants

from .constants import model_schema_constants

class QuerySchema(Schema):
  def __init__(self, OR=True, **kwargs):
    super().__init__(
      **kwargs,
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
        model_schema_constants.AND: Schema(
          server_types=types.ARRAY(),
        ),
        model_schema_constants.OR: Schema(
          server_types=types.ARRAY(),
        ),
      },
    )

class CompositeSchema(Schema):
  def __init__(self, OR=True, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'This key acts as an implicit OR for the children it receives.'
        'Its purpose is to return the fully composed query to the FilterSchema.'
      ),
      server_types=types.ARRAY(),
      template=QuerySchema(),
    )

  def template_responses(self, payload):
    self.template.children.update({
      model_schema_constants.AND: CompositeSchema(OR=False),
      model_schema_constants.OR: CompositeSchema(),
    })

    return self.consolidate_child_responses([
      self.template.respond(payload=child_payload)
      for child_payload in payload
    ])

  def consolidate_child_responses(self, child_responses):
    return child_responses

class FilterSchema(Schema):
  def __init__(self, Model, authorization=None, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description='',
      children={
        model_schema_constants.COMPOSITE: CompositeSchema(),
        model_schema_constants.SORT: Schema(),
        model_schema_constants.PAGINATE: Schema(),
      },
    )

  def consolidate_child_responses(self, child_responses):
    # composite = child_responses.get(model_schema_constants.COMPOSITE)
    #
    # filter_query, composite_errors = construct_filter_query(
    #   composite=composite,
    # )
    #
    # composite.errors.extend(composite_errors)
    #
    # child_responses.update({
    #   model_schema_constants.COMPOSITE: composite,
    # })

    return {
      child_key: child_response
      for child_key, child_response in child_responses.items()
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
