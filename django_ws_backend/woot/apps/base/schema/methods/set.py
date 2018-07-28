
from util.api import (
  Schema, StructureSchema, ArraySchema, IndexedSchema,
  Response, StructureResponse, IndexedResponse,
  types, map_type,
  constants,
)

from ..constants import model_schema_constants
from ..errors import model_schema_errors
from .base import BaseClientResponse, BaseMethodSchema

class NullableSchema(StructureSchema):
  def __init__(self, field, **kwargs):
    self.field = field
    super().__init__(
      **kwargs,
      children={
        model_schema_constants.NULL: Schema(
          types=types.BOOLEAN(),
        ),
      }
    )

  def passes_pre_response_checks(self, payload):
    if not self.field.null:
      self.active_response.add_error(model_schema_errors.NULLABLE_ON_NON_NULLABLE_FIELD(self.field.name))
      return False

    passes_pre_response_checks = super().passes_pre_response_checks(payload)
    if model_schema_constants.NULL not in payload:
      self.active_response.add_error(model_schema_errors.NULLABLE_MUST_CONTAIN_KEY(self.field.name))
      return False

    return passes_pre_response_checks

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

    null_response = self.active_response.get_child(model_schema_constants.NULL)
    if not null_response.value:
      self.active_response.add_error(model_schema_errors.NULLABLE_MUST_BE_TRUE(self.field.name))

class AttributeValueResponse(StructureResponse):
  attribute_value = None
  def get_attribute_value(self):
    return self.attribute_value or self.value

class NullableAttributeSchema(NullableSchema):
  default_response = AttributeValueResponse

class AttributeSetSchema(Schema):
  def __init__(self, attribute, **kwargs):
    self.attribute = attribute
    super().__init__(
      **kwargs,
      description=attribute.verbose_name,
      response=AttributeValueResponse,
      types=[
        map_type(attribute.get_internal_type()),
        types.STRUCTURE(
          schema=NullableAttributeSchema(attribute),
        ),
      ],
    )

class AttributesSetResponse(StructureResponse):
  def get_attributes(self):
    if not self.has_errors():
      attributes = {}
      for attribute in self.parent_schema.model.objects.attributes():
        attribute_response = self.get_child(attribute.name)
        if attribute_response is not None:
          attributes.update({
            attribute.name: attribute_response.get_attribute_value(),
          })

      return attributes

class AttributesSetSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=AttributesSetResponse,
      children={
        attribute.name: AttributeSetSchema(attribute)
        for attribute in Model.objects.attributes()
        if attribute.editable
      },
    )

class RelationshipValueResponse(StructureResponse):
  relationship_value = None
  def get_relationship_value(self):
    return self.relationship_value or self.value

class NullableRelationshipSchema(NullableSchema):
  default_response = RelationshipValueResponse

class RelationshipSetPluralContainer:
  def __init__(self, add=[], remove=[]):
    self.to_add = add
    self.to_remove = remove

class RelationshipSetPluralSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      response=RelationshipValueResponse,
      children={
        model_schema_constants.ADD: ArraySchema(
          template=Schema(
            types=types.UUID(),
          ),
        ),
        model_schema_constants.REMOVE: ArraySchema(
          template=Schema(
            types=types.UUID(),
          ),
        ),
      },
    )

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

    if not self.active_response.has_errors():
      add_response = self.active_response.get_child(model_schema_constants.ADD)
      remove_response = self.active_response.get_child(model_schema_constants.REMOVE)

      if add_response or remove_response:
        self.active_response.relationship_value = RelationshipSetPluralContainer(
          add=(
            [child.value for child in add_response.children]
            if add_response is not None
            else []
          ),
          remove=(
            [child.value for child in remove_response.children]
            if remove_response is not None
            else []
          ),
        )

class RelationshipSetSchema(Schema):
  def __init__(self, relationship, **kwargs):
    self.relationship = relationship
    super().__init__(
      **kwargs,
      description=relationship.name,
      response=RelationshipValueResponse,
      types=(
        [
          types.UUID(),
          types.STRUCTURE(
            schema=NullableRelationshipSchema(relationship),
          ),
        ]
        if relationship.one_to_one or relationship.many_to_one
        else types.STRUCTURE(
          schema=RelationshipSetPluralSchema(),
        )
      ),
    )

class RelationshipsSetResponse(StructureResponse):
  def get_relationships(self):
    if not self.has_errors():
      relationships = {}
      for relationship in self.parent_schema.model.objects.relationships():
        relationship_response = self.get_child(relationship.name)
        if relationship_response is not None:
          relationships.update({
            relationship.name: relationship_response.get_relationship_value(),
          })

      return relationships

class RelationshipsSetSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      response=RelationshipsSetResponse,
      children={
        relationship.name: RelationshipSetSchema(relationship)
        for relationship in Model.objects.relationships()
      },
    )

class PrototypeResponse(StructureResponse):
  def get_prototype(self):
    if not self.has_errors():
      attributes_response = self.force_get_child(model_schema_constants.ATTRIBUTES)
      relationships_response = self.force_get_child(model_schema_constants.RELATIONSHIPS)

      attributes = attributes_response.get_attributes()
      relationships = relationships_response.get_relationships()

      if attributes or relationships:
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
        model_schema_constants.REFERENCE: Schema(types=types.UUID()),
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
      template=PrototypeSchema(Model),
    )

  def responds_to_valid_payload(self, payload):
    super().responds_to_valid_payload(payload)

    if not self.active_response.has_errors():
      for prototype_id, prototype_response in self.active_response.children.items():
        prototype = prototype_response.get_prototype()
        if prototype is not None:
          self.model.objects.update_from_schema(
            id=prototype_id,
            prototype=prototype,
          )

      set_client_payload = {}
      full_queryset = self.model.objects.filter(id__in=self.active_response.children.keys())

      if full_queryset:
        if self.reference_model is not None:
          reference = self.reference_model.objects.from_queryset(full_queryset)
          set_client_payload.update({
            model_schema_constants.REFERENCE: reference,
          })

        self.active_response = SetClientSchema().respond(set_client_payload)
        self.active_response.add_internal_queryset(full_queryset)

        if self.reference_model is not None:
          self.active_response.add_reference(reference)
