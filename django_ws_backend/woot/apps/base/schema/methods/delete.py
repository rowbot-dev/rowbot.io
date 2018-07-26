
from util.api import (
  Schema, IndexedSchema, ArraySchema,
  ArrayResponse,
  types,
)

from ..constants import model_schema_constants
from ..errors import model_schema_errors
from .base import BaseClientResponse, BaseMethodSchema

class DeleteClientSchema(IndexedSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      template=Schema(server_types=types.BOOLEAN()),
    )

class DeleteResponse(ArrayResponse):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)

class DeleteSchema(ArraySchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      template=Schema(
        server_types=types.UUID(),
      ),
    )

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

    if not self.active_response.has_errors():
      confirmed = {}
      for child_response in self.active_response.children:
        number_deleted, deleted_models = self.model.objects.filter(id=child_response.value).delete()
        confirmed.update({
          child_response.value: bool(number_deleted),
        })

      self.active_response = DeleteClientSchema().respond(confirmed)
