
from django.db.models import Q

from util.construct_filter_query import construct_filter_query
from util.api import Schema, Error, Response, types, errors, constants

from .constants import model_schema_constants

class QueryKeyValueNotPresentError(Error):
  def __init__(self):
    return super().__init__(
      code='003',
      name='query_key_value_not_present',
      description='Both key and value must be present',
    )

class QueryAndOrPresentWithKeyValueError(Error):
  def __init__(self):
    return super().__init__(
      code='004',
      name='query_and_or_present_with_key_value',
      description='AND and OR keys must not be present with key or value keys',
    )

class QueryAndOrPresentError(Error):
  def __init__(self):
    return super().__init__(
      code='005',
      name='query_and_or_present',
      description='A query cannot contain both AND and OR keys',
    )

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

  def respond(self, payload=None):
    if payload is None:
      return super().respond(payload=payload)

    self.active_response = self.response()

    if not self.validate_server_type(payload):
      return self.active_response.add_error(errors.SERVER_TYPES(self.server_types))

    invalid_keys = payload.keys() - self.children.keys()
    if invalid_keys:
      return self.active_response.add_error(errors.INVALID_KEYS(invalid_keys))

    self.query_errors(payload)
    if self.active_response.errors:
      return self.active_response

    if model_schema_constants.KEY in payload and model_schema_constants.VALUE in payload:
      key = payload.get(model_schema_constants.KEY)
      value = payload.get(model_schema_constants.VALUE)

      return self.active_response.add_value(Q(**{key: value}))

    if model_schema_constants.AND in payload:
      and_payload = payload.get(model_schema_constants.AND)
      and_child = self.children.get(model_schema_constants.AND)
      and_response = and_child.respond(and_payload)

      if and_response.errors:
        return {model_schema_constants.AND: and_response}

      return and_response

    if model_schema_constants.OR in payload:
      or_payload = payload.get(model_schema_constants.OR)
      or_child = self.children.get(model_schema_constants.OR)
      or_response = or_child.respond(or_payload)

      if or_response.errors:
        return {model_schema_constants.OR: or_response}

      return or_response

  def query_errors(self, payload):
    if model_schema_constants.KEY in payload:
      if model_schema_constants.VALUE not in payload:
        self.active_response.add_error(QueryKeyValueNotPresentError())
      else:
        if model_schema_constants.AND in payload or model_schema_constants.OR in payload:
          self.active_response.add_error(QueryAndOrPresentWithKeyValueError())

    if model_schema_constants.AND in payload and model_schema_constants.OR in payload:
      self.active_response.add_error(QueryAndOrPresentError())

class CompositeResponse(Response):
  def __init__(self, OR=True, **kwargs):
    self.OR = OR
    super().__init__(**kwargs)

  def render_value(self):
    base_query = Q()
    rendered_with_errors = []
    for child in self.value:
      rendered_child = child.render()

      if not isinstance(rendered_child, Q):
        rendered_with_errors.append(rendered_child)
      else:
        if self.OR:
          base_query = base_query | rendered_child
        else:
          base_query = base_query & rendered_child

    if rendered_with_errors:
      return rendered_with_errors

    return base_query

class CompositeSchema(Schema):
  def __init__(self, OR=True, **kwargs):
    self.OR = OR
    super().__init__(
      **kwargs,
      description=(
        'This key acts as an implicit OR for the children it receives.'
        'Its purpose is to return the fully composed query to the FilterSchema.'
      ),
      server_types=types.ARRAY(),
      template=QuerySchema(),
    )

  def response(self):
    return CompositeResponse(OR=self.OR)

  def template_responses(self, payload):
    self.template.children.update({
      model_schema_constants.AND: CompositeSchema(OR=False),
      model_schema_constants.OR: CompositeSchema(),
    })

    return [
      self.template.respond(payload=child_payload)
      for child_payload in payload
    ]

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
    composite_response = child_responses.get(model_schema_constants.COMPOSITE)
    composite_query = composite_response.render()

    print(composite_query)

    return {}

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
