
from util.api import Schema, Response, types, constants

class BaseClientResponse(Response):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.internal_queryset = None
    self.external_querysets = []
    self.reference = None

  def add_internal_queryset(self, queryset):
    self.internal_queryset = queryset

  def add_external_queryset(self, queryset):
    self.external_querysets.append(queryset)

  def add_reference(self, query_reference):
    self.reference = query_reference

class BaseMethodSchema(Schema):
  def __init__(self, **kwargs):
    self.reference_model = None
    super().__init__(**kwargs)

  def add_reference_model(self, reference_model):
    self.reference_model = reference_model
