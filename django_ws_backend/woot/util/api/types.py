
from .constants import constants

class Type():
  description = None

  def __init__(self, description=None):
    self.description = description or self.description

  def __eq__(self, other):
    return self.code == other.code

  def validate(self, value):
    return False

  def render(self):
    return {
      constants.TYPE: self.type,
      constants.DESCRIPTION: self.description,
    }

class Boolean(Type):
  code = '001'
  description = 'A true or false value'
  type = '__boolean'

  def validate(self, value):
    return isinstance(value, bool)

class Integer(Type):
  pass

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

class Time(Type):
  code = '008'
  description = 'A valid timestamp'
  type = '__datetime'

  def validate(self, value):
    return True

class Model(Type):
  pass

class Ref(Type):
  pass

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

def map_type(type_to_map):
  type_map = {
    'CharField': types.STRING(),
    'DateTimeField': types.TIME(),
    'BooleanField': types.BOOLEAN(),
    'UUIDField': types.UUID(),
  }

  return type_map.get(type_to_map)
