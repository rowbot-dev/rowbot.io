
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
        ', '.join([server_type.type for server_type in server_types])
      ),
    )

class InvalidKeys(Error):
  def __init__(self, keys):
    return super().__init__(
      code='002',
      name='invalid_keys',
      description='Invalid keys: [{}]'.format(
        ', '.join([str(key) for key in keys])
      ),
    )

class InvalidIndexes(Error):
  def __init__(self, indexes, index_type):
    return super().__init__(
      code='003',
      name='invalid_indexes',
      description='Invalid indexes: [{}], should be of type {}'.format(
        ', '.join([str(index) for index in indexes]),
        index_type.type,
      ),
    )

class errors:
  SERVER_TYPES = ServerTypes
  INVALID_KEYS = InvalidKeys
  INVALID_INDEXES = InvalidIndexes
