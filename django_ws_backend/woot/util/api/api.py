
from util.api.schema import Schema
from util.api.response import Response

class API():

  def __init__(self, models):
    self.schema = Schema(models)

  def query(self, payload):
    context = payload.get('context', {})
    data = payload.get('data', {})
    message_id = context.get('message')

    response = Response(message_id=message_id)

    authentication = data.get('authentication')
    if authentication:
      schema_authentication = self.schema.authenticate(authentication=authentication)
      response.add_authentication(schema_authentication)

    authorization = context.get('authorization')

    request = data.get('request')
    if request is not None:
      for model_name, query in request.items():
        schema_query = self.schema.query(model_name, query, authorization)
        response.add_query(schema_query)

    should_add_schema = data.get('schema', False)
    if should_add_schema:
      response.add_schema(self.schema.render(authorization=authorization))

    return response

  def greeting(self):
    response = Response()

    response.add_authentication(self.schema.authenticate())
    response.add_schema(self.schema.render())

    return response
