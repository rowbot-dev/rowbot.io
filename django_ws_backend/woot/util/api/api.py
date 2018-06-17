
from util.api.schema import Schema

class API():

  def __init__(self, models, system_information):
    self.models = models
    self.system_information = system_information

  def query(self, payload=None):
    # 1. Spawn response
    schema = Schema(self.models, self.system_information, payload)

    # 2. Check payload against schema
    schema.check_payload()

    if not schema.check_payload_successful:
      return schema.render()

    # 3. Step through authentication process
    schema.check_authentication_process()

    if not schema.check_authentication_process_successful:
      return schema.render()

    # 4. Run query
    schema.run_query()

    # 5. Return response
    return schema.render()

  def greeting(self):
    return self.query()
