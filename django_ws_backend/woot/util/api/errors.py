
class error_constants:
  name = 'name'
  description = 'description'

class Error:
  def __init__(self, code=None, name=None, description=None):
    self.code = code
    self.name = name
    self.description = description

  def render(self):
    return {
      error_constants.name: self.name,
      error_constants.description: self.description,
    }

class Closed(Error):
  def __init__(self):
    return super().__init__(
      code='001',
      name='schema_closed',
      description='Schema accepts no input',
    )

class ServerTypes(Error):
  def __init__(self, server_types=None):
    return super().__init__(
      code='002',
      name='incorrect_payload_type',
      description=(
        'Type of payload must be one of [{}]'.format(
          ', '.join([server_type.type for server_type in server_types])
        )
        if server_types is not None
        else 'Type of payload must be one of the specified server types'
      ),
    )

class InvalidKeys(Error):
  def __init__(self, keys=None):
    return super().__init__(
      code='003',
      name='invalid_keys',
      description=(
        'Invalid keys: [{}]'.format(
          ', '.join([str(key) for key in keys])
        )
        if keys is not None
        else 'Keys must match available keys in schema'
      ),
    )

class InvalidIndexes(Error):
  def __init__(self, indexes=None, index_type=None):
    return super().__init__(
      code='004',
      name='invalid_indexes',
      description=(
        'Invalid indexes: [{}], should be of type {}'.format(
          ', '.join([str(index) for index in indexes]),
          index_type.type,
        )
        if indexes is not None and index_type is not None
        else 'Indexes must match the specified index type'
      ),
    )

class errors:
  CLOSED = Closed
  SERVER_TYPES = ServerTypes
  INVALID_KEYS = InvalidKeys
  INVALID_INDEXES = InvalidIndexes
