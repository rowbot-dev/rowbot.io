
from django.apps import AppConfig

from util.api import (
  Schema, ArraySchema, IndexedSchema,
  Response, ArrayResponse, IndexedResponse,
  types, map_type,
  constants,
)

from apps.base.schema.methods.base import BaseClientResponse, BaseMethodSchema

class RetrieveClientResponse(IndexedResponse, BaseClientResponse):
  pass

class RetrieveClientSchema(IndexedSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=RetrieveClientResponse,
      template=ArraySchema(
        template=Schema(
          types=types.REF(),
        ),
      ),
    )

class RetrieveResponse(ArrayResponse, BaseClientResponse):
  pass

class RetrieveSchema(BaseMethodSchema, ArraySchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    self.models = {}
    super().__init__(
      **kwargs,
      response=RetrieveResponse,
      template=Schema(
        types=types.UUID(),
      )
    )

  def add_model(self, model):
    self.models.update({
      model.__name__: model,
    })

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

    if not self.active_response.has_errors():
      models = {}
      retrieve_client_payload = {}
      for child_response in self.active_response.children:
        reference = self.model.objects.get(id=child_response.value)
        entries = []
        for entry in reference.entries.all():
          entries.append(entry.value)
          model_name, instance_id = tuple(entry.value.split('.'))

          if model_name in models:
            models[model_name].append(instance_id)
          else:
            models[model_name] = [instance_id]

        retrieve_client_payload.update({
          reference._id: entries,
        })

      self.active_response = RetrieveClientSchema().respond(retrieve_client_payload)

      for model_name, model_ids in models.items():
        model_class = self.models.get(model_name)
        model_queryset = model_class.objects.filter(id__in=model_ids)

        self.active_response.add_external_queryset(model_queryset)
