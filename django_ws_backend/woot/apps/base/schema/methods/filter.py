
from django.db.models import Q

from util.pluck import pluck
from util.api import (
  Schema, StructureSchema, ArraySchema, IndexedSchema,
  Response, StructureResponse, ArrayResponse,
  types,
  constants,
)

from ..constants import model_schema_constants
from ..errors import model_schema_errors
from .base import BaseClientResponse, BaseMethodSchema

class QueryResponse(StructureResponse):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.key_value = False

  def add_child(self, child_key, child_response):
    super().add_child(child_key, child_response)
    if not self.key_value and child_response.has_errors():
      self.has_child_errors = True

  def get_query(self):
    if self.key_value:
      key_response = self.children.get(model_schema_constants.KEY)
      value_response = self.children.get(model_schema_constants.VALUE)

      if not key_response.has_errors() and not value_response.has_errors():
        return Q(**{key_response.render(): value_response.render()})
    else:
      [response] = self.children.values()
      if not response.has_errors():
        return response.get_query()

class QuerySchema(StructureSchema):
  available_errors = StructureSchema.available_errors + [
    model_schema_errors.QUERY_KEY_VALUE_NOT_PRESENT(),
    model_schema_errors.QUERY_AND_OR_PRESENT_WITH_KEY_VALUE(),
    model_schema_errors.QUERY_AND_OR_PRESENT(),
    model_schema_errors.FIELD_DOES_NOT_EXIST(),
    model_schema_errors.MULTIPLE_DIRECTIVES_FOR_NON_RELATED_FIELD(),
    model_schema_errors.INVALID_QUERY_DIRECTIVE(),
  ]

  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=QueryResponse,
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

  def passes_pre_response_checks(self, payload):
    passes_pre_response_checks = super().passes_pre_response_checks(payload)
    if model_schema_constants.KEY in payload or model_schema_constants.VALUE in payload:
      if model_schema_constants.KEY not in payload or model_schema_constants.VALUE not in payload:
        self.active_response.add_error(model_schema_errors.QUERY_KEY_VALUE_NOT_PRESENT())

      if model_schema_constants.AND in payload or model_schema_constants.OR in payload:
        self.active_response.add_error(model_schema_errors.QUERY_AND_OR_PRESENT_WITH_KEY_VALUE())

      if self.active_response.has_errors():
        return False

      self.active_response.key_value = True
      key, value = pluck(payload, model_schema_constants.KEY, model_schema_constants.VALUE)
      model_query_check_errors = self.model.objects.query_check(key, value)
      if model_query_check_errors:
        for error in model_query_check_errors:
          self.active_response.add_error(error)
        return False

    if model_schema_constants.AND in payload and model_schema_constants.OR in payload:
      self.active_response.add_error(model_schema_errors.QUERY_AND_OR_PRESENT())
      return False

    return passes_pre_response_checks

class CompositeResponse(ArrayResponse):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.OR = parent_schema.OR

  def add_child(self, child_response):
    super().add_child(child_response)
    if child_response.has_errors():
      self.has_child_errors = True

  def render_value(self):
    if self.has_child_errors:
      self.rendered = []
      for child_response in self.children:
        if child_response.has_child_errors:
          self.rendered.append(child_response.render())
        else:
          self.rendered.append(child_response.render_errors())

  def get_query(self):
    if not self.has_child_errors:
      query = Q()
      for child in self.children:
        if self.OR:
          query = query | child.get_query()
        else:
          query = query & child.get_query()

      return query

class CompositeSchema(ArraySchema):
  def __init__(self, Model, OR=True, **kwargs):
    super().__init__(
      **kwargs,
      response=CompositeResponse,
      template=QuerySchema(Model),
    )
    self.model = Model
    self.OR = OR

  def responds_to_valid_payload(self, payload):
    self.template.children.update({
      model_schema_constants.AND: CompositeSchema(self.model, OR=False),
      model_schema_constants.OR: CompositeSchema(self.model),
    })
    super().responds_to_valid_payload(payload)

class FilterClientResponse(StructureResponse, BaseClientResponse):
  pass

class FilterClientSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=FilterClientResponse,
      children={
        model_schema_constants.COUNT: Schema(server_types=types.INTEGER()),
        model_schema_constants.REFERENCE: Schema(server_types=types.UUID()),
      },
    )

class FilterResponse(StructureResponse, BaseClientResponse):
  pass

class FilterSchema(BaseMethodSchema, StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=FilterResponse,
      children={
        model_schema_constants.COMPOSITE: CompositeSchema(Model),
      },
    )

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

    composite_response = self.active_response.force_get_child(model_schema_constants.COMPOSITE)
    composite_query = composite_response.get_query()

    if composite_query is not None:
      queryset = self.model.objects.filter(composite_query)
      filter_client_payload = {
        model_schema_constants.COUNT: queryset.count(),
      }

      if self.reference_model is not None:
        query_reference = self.reference_model.objects.from_queryset(queryset)
        filter_client_payload.update({
          model_schema_constants.REFERENCE: query_reference,
        })

      self.active_response = FilterClientSchema().respond(filter_client_payload)
      self.active_response.add_internal_queryset(queryset)

      if self.reference_model is not None:
        self.active_response.add_reference(query_reference)
