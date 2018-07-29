
from util.api import (
  Schema, StructureSchema, ArraySchema,
  StructureResponse,
  types,
)

from ..constants import model_schema_constants
from .base import BaseClientResponse, BaseMethodSchema

class GetClientResponse(StructureResponse, BaseClientResponse):
  pass

class GetClientSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=GetClientResponse,
      children={
        model_schema_constants.REFERENCE: Schema(types=types.UUID()),
      },
    )

class GetResponse(StructureResponse, BaseClientResponse):
  pass

class GetSchema(BaseMethodSchema, ArraySchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=GetResponse,
      template=Schema(
        types=types.UUID(),
      ),
    )

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

    if not self.active_response.has_errors():
      ids = [child.value for child in self.active_response.children]
      queryset = self.model.objects.filter(id__in=ids)

      get_client_payload = {}
      if self.reference_model is not None:
        query_reference = self.reference_model.objects.from_queryset(queryset)
        get_client_payload.update({
          model_schema_constants.REFERENCE: query_reference,
        })

      self.active_response = GetClientSchema().respond(get_client_payload)
      self.active_response.add_internal_queryset(queryset)

      if self.reference_model is not None:
        self.active_response.add_reference(query_reference)
