
from util.api import (
  Schema, StructureSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types,
  constants,
)

from apps.base.schema.constants import model_schema_constants
from apps.base.schema.methods.base import BaseClientResponse, BaseMethodSchema

from .constants import role_schema_constants

class RoleSomethingClientSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      children={
        'hello': Schema(types=types.INTEGER()),
        'goodbye': Schema(types=types.INTEGER()),
      },
    )

class RoleSomethingSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      client=RoleSomethingClientSchema(),
      children={
        'argument1': Schema(types=types.INTEGER()),
        'argument2': Schema(types=types.INTEGER()),
      },
    )

  def responds_to_client(self):
    pass

class RoleInstanceMethodsResponse(StructureResponse, BaseClientResponse):
  pass

class RoleInstanceMethodsSchema(BaseMethodSchema, StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description='No available instance methods, sir.',
      response=RoleInstanceMethodsResponse,
      children={
        role_schema_constants.SOMETHING: RoleSomethingSchema(),
      },
    )

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

class RoleRunResponse(IndexedResponse, BaseClientResponse):
  pass

class RoleRunSchema(BaseMethodSchema, IndexedSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=RoleRunResponse,
      template=RoleInstanceMethodsSchema(),
    )

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

    if not self.active_response.has_errors():
      for instance_id, instance_methods_response in self.active_response.children.items():
        for instance_method_name, instance_method_arguments in instance_methods_response.children.items():
          instance_method_output = self.model.objects.run_instance_method(
            id=instance_id,
            method_name=instance_method_name,
            arguments=instance_method_arguments.render(),
          )

          instance_methods_response.children.update({
            instance_method_name: instance_method_arguments.client_schema.respond(instance_method_output)
          })
