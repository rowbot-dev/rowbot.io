
from util.api import StructureSchema

from ..constants import model_schema_constants
from .filter import FilterSchema
from .create import CreateSchema
from .delete import DeleteSchema
from .get import GetSchema
from .set import SetSchema

class ModelMethodsSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description='No available model methods',
      children={
        model_schema_constants.FILTER: FilterSchema(Model),
        model_schema_constants.CREATE: CreateSchema(Model),
        model_schema_constants.DELETE: DeleteSchema(Model),
        model_schema_constants.GET: GetSchema(Model),
        model_schema_constants.SET: SetSchema(Model),
      },
    )

  def add_reference_model(self, reference_model):
    self.reference_model = reference_model
    for child in self.children.values():
      child.add_reference_model(reference_model)
