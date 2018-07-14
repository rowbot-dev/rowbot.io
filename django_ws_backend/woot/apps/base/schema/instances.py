
from util.api import (
  Schema, StructureSchema, IndexedSchema,
  StructureResponse, IndexedResponse,
  types,
  errors,
  constants,
)

from .constants import model_schema_constants

class InstanceResponse(StructureResponse):
  pass

class InstanceSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=InstanceResponse,
      children={
        model_schema_constants.ATTRIBUTES: IndexedSchema(
          index_type=types.STRING(),
          client=IndexedSchema(
            index_type=types.STRING(),
            template=Schema(server_types=types.ANY()),
          ),
          template=StructureSchema(
            children={
              model_schema_constants.GET: Schema(
                description='Interface to refresh the local value of an attribute',
                server_types=types.BOOLEAN('A value of true will update the attribute from the system'),
              ),
              model_schema_constants.SET: Schema(
                description='Interface to set the remote value of the attribute',
                server_types=types.ANY('Any value will be typechecked against the type specified in the attribute schema'),
              ),
            },
          ),
        ),
        # model_schema_constants.RELATIONSHIPS: IndexedSchema(
        #   index_type=types.STRING(),
        #   template=StructureSchema(
        #     children={
        #       model_schema_constants.GET: Schema(
        #         description='Interface to refresh the local value of an attribute',
        #         server_types=types.BOOLEAN('A value of true will update the attribute from the system'),
        #       ),
        #       model_schema_constants.SET: Schema(
        #         description='Interface to set the remote value of the attribute',
        #         server_types=types.ANY('Any value will be typechecked against the type specified in the attribute schema'),
        #       ),
        #     },
        #   ),
        # ),
        # model_schema_constants.METHODS: Model.objects.schema_instance_methods(),
      },
    )

  def response_from_model_instance(self, instance, attributes):
    response = self.get_response()

    serialized_instance = self.model.objects.serialize(instance, attributes=attributes)

    serialized_instance_attributes = serialized_instance.get(model_schema_constants.ATTRIBUTES)
    attributes_client_schema = self.children.get(model_schema_constants.ATTRIBUTES).client
    attributes_client_response = attributes_client_schema.respond(serialized_instance_attributes)

    response.children.update({
      model_schema_constants.ATTRIBUTES: attributes_client_response,
    })

    return response

class InstancesResponse(IndexedResponse):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)

  def add_instances(self, instances, attributes):
    for instance in instances:
      self.add_child(instance._id, self.template_schema.response_from_model_instance(instance, attributes))

  def add_attributes(self, attributes):
    self.attributes = attributes

class InstancesSchema(IndexedSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(
      **kwargs,
      response=InstancesResponse,
      template=InstanceSchema(Model),
    )
