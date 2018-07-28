
from util.is_valid_uuid import is_valid_uuid

from .constants import constants

class Type():
  description = None
  schema = None

  def __init__(self, description=None, schema=None):
    self.description = description or self.description
    self.schema = schema or self.schema

  def __eq__(self, other):
    return self.code == other.code

  def validate(self, value):
    return False

  def render(self):
    rendered = {
      constants.TYPE: self.type,
      constants.DESCRIPTION: self.description,
    }

    if self.schema is not None:
      rendered.update({
        constants.SCHEMA: self.schema.respond().render(),
      })

    return rendered

class Boolean(Type):
  code = '001'
  description = 'A true or false value'
  type = '__boolean'

  def validate(self, value):
    return isinstance(value, bool)

class Integer(Type):
  code = '002'
  description = 'A whole number value'
  type = '__integer'

  def validate(self, value):
    return isinstance(value, int)

class Float(Type):
  pass

class String(Type):
  code = '004'
  description = 'A string of characters'
  type = '__string'

  def validate(self, value):
    return isinstance(value, str)

class Structure(Type):
  code = '005'
  description = 'A JSON object'
  type = '__structure'

  def validate(self, value):
    return isinstance(value, dict)

class Array(Type):
  code = '006'
  description = 'A JSON array'
  type = '__array'

  def validate(self, value):
    return isinstance(value, list)

class UUID(Type):
  code = '007'
  description = 'A valid UUID'
  type = '__uuid'

  def validate(self, value):
    return is_valid_uuid(value)

class Time(Type):
  code = '008'
  description = 'A valid timestamp'
  type = '__datetime'

  def validate(self, value):
    return True

class Model(Type):
  pass

class Ref(Type):
  code = '010'
  description = 'A string composed of a model name and uuid separated by a point'
  type = '__ref'

  def validate(self, value):
    if isinstance(value, str):
      split_value = value.split('.')
      if len(split_value) == 2:
        [model_name, uuid_value] = split_value
        return is_valid_uuid(uuid_value)
    return False

class Enum(Type):
  def __init__(self, *options):
    self.options = options

class Immutable(Type):
  pass

class Any(Type):
  code = '013'
  description = 'Any value'
  type = '__any'

  def validate(self, value):
    return True

class Null(Type):
  code = '014'
  description = 'Null value'
  type = '__null'

  def validate(self, value):
    return value == constants.NULL

class types:
  BOOLEAN = Boolean
  MODEL = Model
  STRUCTURE = Structure
  ARRAY = Array
  INTEGER = Integer
  FLOAT = Float
  STRING = String
  UUID = UUID
  TIME = Time
  REF = Ref
  ENUM = Enum
  IMMUTABLE = Immutable
  ANY = Any
  NULL = Null

def map_type(type_to_map):
  type_map = {
    'CharField': types.STRING(),
    'DateTimeField': types.TIME(),
    'BooleanField': types.BOOLEAN(),
    'UUIDField': types.UUID(),
  }

  return type_map.get(type_to_map)
