
from util.api.schema import Schema

class API():

  def __init__(self, models, system_information):
    self.schema = Schema(models, system_information)

  def query(self, payload=None):
    return self.schema.query(payload)

  def greeting(self):
    return self.query()
