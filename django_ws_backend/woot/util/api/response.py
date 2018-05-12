
from util.api.errors import Errors
from util.merge import merge

class Response():

  def __init__(self, message_id):
    self.id = message_id
    self.payload = {}

  def add_authentication(self, authentication):
    if authentication:
      self.payload = merge(
        self.payload,
        {
          'context': {
            'authentication': authentication,
          },
        },
      )

  def add_schema(self, schema):
    if schema:
      self.payload = merge(self.payload, schema)

  def add_query(self, query):
    if query:
      self.payload = merge(self.payload, query)

  def render(self):
    return merge(
      self.payload,
      {
        'context': {
          'message': self.id,
        },
      },
    )
