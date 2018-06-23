
from util.force_array import force_array

from .errors import errors
from .response import Response

class Entry():
  def __init__(self, options):
    self.description = options.get('description')
    self.server = force_array(options.get('server'))
    self.client = options.get('client')
    self.children = options.get('children')

  def query(self, payload):
    response = Response({
      'description': self.description,
      'server': self.server,
      'client': self.client,
    })

    # add errors for unrecognised keys
    unrecognised_keys = self.children.keys() - payload.keys()
    if unrecognised_keys:
      for key in unrecognised_keys:
        response.add_error(errors.UNRECOGNISED(key))

      return response

    # check server types
    for server_type in self.server:
      validated = server_type.validate(payload)
      if not validated:
        response.add_error(errors.TYPE(server_type))

    if response.has_errors:
      return response

    # if there are no children, run the specific query for this level
    if not self.children:
      response.set_value(self.specific_query(payload))

    # send query to children
    for child_key, child in self.children.items():
      child_payload = payload.get(child_key)
      response.add_child(child_key, child.query(child_payload))

    return response
