
import json

from django.db.models import Q

from util.construct_filter_query import construct_filter_query
from util.api import (
  Schema, StructureSchema, ArraySchema, IndexedSchema,
  Response, StructureResponse, ArrayResponse,
  types,
  errors, Error,
  constants,
)

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

class QueryResponse(StructureResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.has_child_errors = False
    self.key_value = False

  def add_child(self, child_key, child_response):
    super().add_child(child_key, child_response)
    if not self.key_value and (child_response.errors or child_response.has_child_errors):
      self.has_child_errors = True

  def render_value(self):
    super().render_value()
    if self.key_value:
      key_response = self.children.get(model_schema_constants.KEY)
      value_response = self.children.get(model_schema_constants.VALUE)

      if not key_response.errors and not value_response.errors:
        self.rendered = Q(**{key_response.render(): value_response.render()})
    else:
      [response] = self.children.values()
      if not response.errors and not response.has_child_errors:
        self.rendered = response.render()

class QuerySchema(StructureSchema):
  def __init__(self, OR=True, **kwargs):
    super().__init__(
      **kwargs,
      children={
        model_schema_constants.KEY: Schema(
          description='',
          server_types=types.STRING(),
        ),
        model_schema_constants.VALUE: Schema(
          description='',
          server_types=types.STRING(),
        ),
        model_schema_constants.AND: ArraySchema(
          template=Schema(),
        ),
        model_schema_constants.OR: ArraySchema(
          template=Schema(),
        ),
      },
    )

  def response(self):
    return QueryResponse(description=self.description, server_types=self.server_types)

  def passes_pre_response_checks(self, payload):
    passes_pre_response_checks = super().passes_pre_response_checks(payload)
    if model_schema_constants.KEY in payload:
      if model_schema_constants.VALUE not in payload:
        self.active_response.add_error(QueryKeyValueNotPresentError())
        return False
      else:
        if model_schema_constants.AND in payload or model_schema_constants.OR in payload:
          self.active_response.add_error(QueryAndOrPresentWithKeyValueError())
          return False

      self.active_response.key_value = True

    if model_schema_constants.AND in payload and model_schema_constants.OR in payload:
      self.active_response.add_error(QueryAndOrPresentError())
      return False

    return passes_pre_response_checks

class CompositeResponse(ArrayResponse):
  def __init__(self, OR=True, **kwargs):
    super().__init__(**kwargs)
    self.has_child_errors = False
    self.OR = OR

  def add_child(self, child_response):
    super().add_child(child_response)
    if child_response.errors or child_response.has_child_errors:
      self.has_child_errors = True

  def render_value(self):
    if self.has_child_errors:
      self.rendered = []
      for child_response in self.children:
        if child_response.has_child_errors:
          self.rendered.append(child_response.render())
        else:
          self.rendered.append(child_response.render_errors())
    else:
      self.rendered = Q()
      for child in self.children:
        if self.OR:
          self.rendered = self.rendered | child.render()
        else:
          self.rendered = self.rendered & child.render()

class CompositeSchema(ArraySchema):
  def __init__(self, OR=True, query_description=None, **kwargs):
    self.OR = OR
    super().__init__(template=QuerySchema(description=query_description), **kwargs)

  def response(self):
    return CompositeResponse(
      OR=self.OR,
      description=self.description,
      server_types=self.server_types,
    )

  def responds_to_valid_payload(self, payload):
    self.template.children.update({
      model_schema_constants.AND: CompositeSchema(OR=False, description='C2', query_description='Q2'),
      model_schema_constants.OR: CompositeSchema(),
    })
    super().responds_to_valid_payload(payload)

class FilterSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      children={
        model_schema_constants.COMPOSITE: CompositeSchema(
          description='C1',
          query_description='Q1',
        ),
        # model_schema_constants.SORT: Schema(),
        # model_schema_constants.PAGINATE: Schema(),
      },
    )

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)
    composite_response = self.active_response.children.get(model_schema_constants.COMPOSITE)

    self.active_response.children = {}
    if composite_response.errors or composite_response.has_child_errors:
      self.active_response.children.update({
        model_schema_constants.COMPOSITE: composite_response,
      })
    else:
      print(composite_response.render())


class ModelMethodsSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description='No available model methods',
      children={
        model_schema_constants.FILTER: FilterSchema(Model),
      },
    )
