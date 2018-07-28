
from util.api import (
  Schema, StructureSchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
)

from ..constants import model_schema_constants
from ..errors import model_schema_errors
from .base import BaseClientResponse, BaseMethodSchema

class AttributeSetSchema(Schema):
  def __init__(self, attribute, **kwargs):
    self.attribute = attribute
    super().__init__(
      **kwargs,
      description=attribute.verbose_name,
      server_types=map_type(attribute.get_internal_type()),
    )

class AttributesSetResponse(StructureResponse):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)

  def add_child(self, child_key, child_response):
    super().add_child(child_key, child_response)
    if child_response.has_errors():
      self.has_child_errors = True

  def get_attributes(self):
    if not self.has_errors() and not self.is_empty:
      return self.render()
    return {}

class AttributesSetSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    self.non_nullable = {
      attribute.name
      for attribute in Model.objects.attributes()
      if (
        attribute.editable
        and not attribute.has_default()
        and not attribute.null
      )
    }
    super().__init__(
      **kwargs,
      response=AttributesSetResponse,
      children={
        attribute.name: AttributeSetSchema(attribute)
        for attribute in Model.objects.attributes()
        if attribute.editable
      },
    )

  def passes_pre_response_checks(self, payload):
    passes_pre_response_checks = super().passes_pre_response_checks(payload)
    non_nullable_not_included = self.non_nullable - payload.keys()
    if non_nullable_not_included:
      self.active_response.add_error(model_schema_errors.NON_NULLABLE_NOT_INCLUDED(non_nullable_not_included))
      return False

    return passes_pre_response_checks

class RelationshipSetSchema(Schema):
  def __init__(self, relationship, **kwargs):
    self.relationship = relationship
    super().__init__(
      **kwargs,
      description=relationship.name,
      server_types=(
        types.UUID()
        if relationship.one_to_one or relationship.many_to_one
        else types.ARRAY()
      ),
    )

class RelationshipsSetResponse(StructureResponse):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)

  def add_child(self, child_key, child_response):
    super().add_child(child_key, child_response)
    if child_response.has_errors():
      self.has_child_errors = True

  def get_relationships(self):
    if not self.has_errors() and not self.is_empty:
      return self.render()
    return {}

class RelationshipsSetSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    self.non_nullable = {
      relationship.name
      for relationship in Model.objects.relationships()
      if (
        relationship.editable
        and not relationship.has_default()
        and not relationship.null
        and not relationship.one_to_many
        and not relationship.many_to_many
      )
    }
    super().__init__(
      **kwargs,
      response=RelationshipsSetResponse,
      children={
        relationship.name: RelationshipSetSchema(relationship)
        for relationship in Model.objects.relationships()
      },
    )

  def add_child(self, child_response):
    super().add_child(child_response)
    if child_response.has_errors():
      self.has_child_errors = True

  def passes_pre_response_checks(self, payload):
    passes_pre_response_checks = super().passes_pre_response_checks(payload)
    non_nullable_not_included = self.non_nullable - payload.keys()
    if non_nullable_not_included:
      self.active_response.add_error(model_schema_errors.NON_NULLABLE_NOT_INCLUDED(non_nullable_not_included))
      return False

    return passes_pre_response_checks

class PrototypeResponse(StructureResponse):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)

  def add_child(self, child_key, child_response):
    super().add_child(child_key, child_response)
    if child_response.has_errors():
      self.has_child_errors = True

  def get_prototype(self):
    if not self.has_errors():
      attributes_response = self.force_get_child(model_schema_constants.ATTRIBUTES)
      relationships_response = self.force_get_child(model_schema_constants.RELATIONSHIPS)

      attributes = attributes_response.get_attributes()
      relationships = relationships_response.get_relationships()

      if attributes and relationships:
        prototype = {}
        for attribute_name, attribute in attributes.items():
          prototype.update({attribute_name: attribute})

        for relationship_name, relationship in relationships.items():
          prototype.update({relationship_name: relationship})

        return prototype

class PrototypeSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=PrototypeResponse,
      children={
        model_schema_constants.ATTRIBUTES: AttributesSetSchema(Model),
        model_schema_constants.RELATIONSHIPS: RelationshipsSetSchema(Model),
      },
    )

class SetClientResponse(StructureResponse, BaseClientResponse):
  pass

class SetClientSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=SetClientResponse,
      children={
        model_schema_constants.REFERENCE: Schema(server_types=types.UUID()),
        model_schema_constants.TEMPORARY_IDS: IndexedSchema(
          index_type=types.STRING(),
          template=Schema(server_types=types.UUID()),
        ),
      },
    )

class SetResponse(IndexedResponse, BaseClientResponse):
  pass

class SetSchema(BaseMethodSchema, IndexedSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=SetResponse,
      index_type=types.STRING(),
      template=PrototypeSchema(Model),
    )

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

    # 1. need to be able to set a field to null
    # 2. need to be able to remove relationships from one-to-many or many-to-many.
    # 3.

    # temporary_ids = {}
    # created = []
    # for prototype_temporary_id, prototype_response in self.active_response.children.items():
    #   prototype = prototype_response.get_prototype()
    #   if prototype is not None:
    #     instance = self.model.objects.create_from_schema(**prototype)
    #     created.append(instance)
    #     temporary_ids.update({
    #       prototype_temporary_id: instance._id,
    #     })
    #
    # if created:
    #   create_client_payload = {
    #     model_schema_constants.TEMPORARY_IDS: temporary_ids,
    #   }
    #   if self.reference_model is not None:
    #     reference = self.reference_model.objects.from_queryset(created)
    #     create_client_payload.update({
    #       model_schema_constants.REFERENCE: reference,
    #     })
    #
    #   self.active_response = SetClientSchema().respond(create_client_payload)
    #   self.active_response.add_internal_queryset(created)
    #
    #   if self.reference_model is not None:
    #     self.active_response.add_reference(reference)
