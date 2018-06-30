
class Error:
  def __init__(self, code=None, name=None, description=None):
    self.code = code
    self.name = name
    self.description = description

  def render(self):
    return {
      'name': self.name,
      'description': self.description,
    }

class ServerTypes(Error):
  def __init__(self, server_types):
    return super().__init__(
      code='001',
      name='incorrect_payload_type',
      description='Type of payload must be one of [{}]'.format(
        ', '.join([type.render() for type in server_types])
      ),
    )

class UnrecognisedKeys(Error):
  def __init__(self, keys):
    return super().__init__(
      code='002',
      name='unrecognised_keys',
      description='Unrecognised keys: [{}]'.format(
        ', '.join(keys)
      ),
    )

class errors:
  SERVER_TYPES = ServerTypes
  INVALID_KEYS = UnrecognisedKeys
