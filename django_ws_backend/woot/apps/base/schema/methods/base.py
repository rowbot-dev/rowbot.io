
from util.api import StructureSchema, types, constants

class BaseMethodSchema(StructureSchema):
  def add_reference_group_model(self, reference_group_model):
    self.reference_group_model = reference_group_model
