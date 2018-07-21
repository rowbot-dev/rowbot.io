
from util.api import StructureSchema

from ..constants import model_schema_constants
from .filter import FilterSchema
from .create import CreateSchema

class ModelMethodsSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description='No available model methods',
      children={
        model_schema_constants.FILTER: FilterSchema(Model),
        model_schema_constants.CREATE: CreateSchema(Model),
      },
    )

  def add_reference_model(self, reference_model):
    self.reference_model = reference_model
    for child in self.children.values():
      child.add_reference_model(reference_model)
