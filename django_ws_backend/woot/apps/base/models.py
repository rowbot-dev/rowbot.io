
import uuid

from django.db import models
from django.db.models import Q
from django.core.exceptions import FieldDoesNotExist

from util.api import Schema, StructureSchema, Error, constants

from .constants import query_directives, is_valid_query_directive
from .schema import (
  model_schema_constants,
  model_schema_errors,
  SchemaManagerMixin,
)

class models_constants:
  ID = 'id'

class Manager(models.Manager, SchemaManagerMixin):
  use_for_related_fields = True

  def attributes(self):
    return [
      field
      for field in self.model._meta.get_fields()
      if (
        not field.is_relation
        and field.name != models_constants.ID
      )
    ]

  def relationships(self):
    return [
      field
      for field in self.model._meta.get_fields()
      if (
        field.is_relation
        or (
          field.auto_created
          and not field.concrete
        )
      )
    ]

  def get(self, **kwargs):
    filtered = super().filter(**kwargs)
    if filtered.exists():
      return filtered[0]
    return None

  def filter(self, *args, **kwargs):
    return super().filter(*args, **kwargs)

  def create_from_schema(self, **kwargs):
    add_after_creation = {}
    modified_kwargs = {}
    for property_key, property in kwargs.items():
      field = self.model._meta.get_field(property_key)
      if field.is_relation:
        if field.one_to_one or field.many_to_one:
          related_object = field.related_model.objects.get(id=property)
          modified_kwargs.update({
            property_key: related_object,
          })
        elif field.one_to_many or field.many_to_many:
          related_objects = field.related_model.objects.filter(id__in=property)
          add_after_creation.update({
            property_key: related_objects,
          })
      else:
        modified_kwargs.update({property_key: property})

    created = super().create(**modified_kwargs)
    for property_key, property in add_after_creation.items():
      for related_object in property:
        relationship = getattr(created, property_key)
        relationship.add(related_object)

    return created

  def update_from_schema(self, id=None, prototype={}):
    print(prototype)
    if id is not None:
      instance = self.get(id=id)

      for property_key, property in prototype.items():
        field = self.model._meta.get_field(property_key)
        if field.is_relation:
          if field.one_to_one or field.many_to_one:
            related_object = field.related_model.objects.get(id=property)
            setattr(instance, property_key, related_object)
          elif field.one_to_many or field.many_to_many:
            related_field = getattr(instance, property_key)
            related_objects_to_add = field.related_model.objects.filter(id__in=property.to_add)
            for item in related_objects_to_add:
              related_field.add(item)

            related_objects_to_remove = field.related_model.objects.filter(id__in=property.to_remove)
            for item in related_objects_to_remove:
              related_field.remove(item)
        else:
          setattr(instance, property_key, property)

      instance.save()

  def query_check(self, key, value):
    tokens = key.split(query_directives.JOIN)
    query_errors = []
    field_name, rest_of_tokens = tokens[0], tokens[1:]

    try:
      field = self.model._meta.get_field(field_name)
    except FieldDoesNotExist:
      query_errors.append(model_schema_errors.FIELD_DOES_NOT_EXIST(field=field_name, model=self.model._meta.object_name))
      return query_errors

    if field.is_relation:
      related_field_errors = field.related_model.objects.query_check(query_directives.JOIN.join(rest_of_tokens), value)
      if related_field_errors:
        query_errors.extend(related_field_errors)
        return query_errors
    else:
      if len(rest_of_tokens) > 1:
        query_errors.append(model_schema_errors.MULTIPLE_DIRECTIVES_FOR_NON_RELATED_FIELD(field=field_name, directives=rest_of_tokens))
        return query_errors
      elif len(rest_of_tokens) == 1:
        [directive] = rest_of_tokens
        if not is_valid_query_directive(directive):
          query_errors.append(model_schema_errors.INVALID_QUERY_DIRECTIVE(field=field_name, directive=directive))
          return query_errors

    return query_errors

  def serialize(self, instance, attributes=None, relationships=None):
    return {
      model_schema_constants.ATTRIBUTES: self.serialize_attributes(instance, attributes=attributes),
      model_schema_constants.RELATIONSHIPS: self.serialize_relationships(instance, relationships=relationships),
    }

  def serialize_attributes(self, instance, attributes=None):
    return {
      attribute_field.name: str(getattr(instance, attribute_field.name))
      for attribute_field
      in self.attributes()
      if attributes is None or attribute_field.name in attributes
    }

  def serialize_relationships(self, instance, relationships=None):
    return {
      relationship_field.name: (
        (
          getattr(instance, relationship_field.name)._ref
          if getattr(instance, relationship_field.name) is not None
          else constants.NULL
        )
        if relationship_field.one_to_one or relationship_field.many_to_one
        else [
          related_object._ref
          for related_object
          in getattr(instance, relationship_field.name).all()
        ]
      )
      for relationship_field
      in self.relationships()
      if relationships is None or relationship_field.name in relationships
    }

class Model(models.Model):

  objects = Manager()

  class Meta:
    abstract = True

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  date_created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Date created')

  @property
  def _id(self):
    return self.id.hex

  @property
  def _ref(self):
    return '{}.{}'.format(self.__class__.__name__, self._id)

class MockParentModel(Model):
  class Meta:
    app_label = 'base'

  name = models.CharField(max_length=255)

class MockModel(Model):
  class Meta:
    app_label = 'base'

  parent = models.ForeignKey(MockParentModel, related_name='children', on_delete=models.CASCADE, null=True)
  under = models.ManyToManyField('self', related_name='over', symmetrical=False)
  name = models.CharField(max_length=255)
