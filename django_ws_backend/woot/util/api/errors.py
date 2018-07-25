
class error_constants:
  name = 'name'
  description = 'description'

class Error:
  code = '000'
  name = None
  description = None

  def render(self):
    return {
      error_constants.name: self.name,
      error_constants.description: self.description,
    }

class Closed(Error):
  code = '001'
  name = 'schema_closed'
  description = 'Schema accepts no input'

class ServerTypes(Error):
  code = '002'
  name = 'incorrect_payload_type'
  description = 'Type of payload must be one of the specified server types'
  description_with_arguments = 'Type of payload must be one of [{}]'

  def __init__(self, server_types=None):
    self.description = (
      self.description_with_arguments.format(
        ', '.join([server_type.type for server_type in server_types])
      )
      if server_types is not None
      else self.description
    )

class InvalidKeys(Error):
  code = '003'
  name = 'invalid_keys'
  description = 'Keys must match available keys in schema'
  description_with_arguments = 'Invalid keys: [{}]'

  def __init__(self, keys=None):
    self.description = (
      self.description_with_arguments.format(
        ', '.join([str(key) for key in keys])
      )
      if keys is not None
      else self.description
    )

class InvalidIndexes(Error):
  code = '004'
  name = 'invalid_indexes'
  description = 'Indexes must match the specified index type'
  description_with_arguments = 'Invalid indexes: [{}], should be of type {}'

  def __init__(self, indexes=None, index_type=None):
    self.description = (
      self.description_with_arguments.format(
        ', '.join([str(index) for index in indexes]),
        index_type.type,
      )
      if indexes is not None and index_type is not None
      else self.description
    )

class errors:
  CLOSED = Closed
  SERVER_TYPES = ServerTypes
  INVALID_KEYS = InvalidKeys
  INVALID_INDEXES = InvalidIndexes
