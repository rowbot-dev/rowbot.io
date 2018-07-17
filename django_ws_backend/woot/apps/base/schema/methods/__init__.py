
from util.api import StructureSchema

from ..constants import model_schema_constants
from .filter import FilterSchema

class ModelMethodsSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description='No available model methods',
      children={
        model_schema_constants.FILTER: FilterSchema(Model),
      },
    )
