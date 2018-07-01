
class Type():
  description = None

  def __init__(self, description=None):
    self.description = description or self.description

  def __eq__(self, other):
    return self._type == other._type

  def validate(self, value):
    return False

  def render(self):
    return self._type

class Boolean(Type):
  description = 'A true or false value'
  _type = '__boolean'

  def validate(self, value):
    return isinstance(value, bool)

class Model(Type):
  pass

class Structure(Type):
  description = 'A JSON object'
  _type = '__structure'

  def validate(self, value):
    return isinstance(value, dict)

class Array(Type):
  pass

class Integer(Type):
  pass

class Float(Type):
  pass

class String(Type):
  description = 'A string of characters'
  _type = '__string'

  def validate(self, value):
    return isinstance(value, str)

class UUID(Type):
  description = 'A valid UUID'
  _type = '__uuid'

class Time(Type):
  description = 'A valid timestamp'
  _type = '__time'

class Ref(Type):
  pass

class Enum(Type):
  def __init__(self, *options):
    self.options = options

class Immutable(Type):
  pass

class Any(Type):
  description = 'Any value'
  _type = '__any'

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

  def as_entries():
    pass

def map_type(type_to_map):
  type_map = {
    'CharField': types.STRING(),
    'DateTimeField': types.TIME(),
    'BooleanField': types.BOOLEAN(),
    'UUIDField': types.UUID(),
  }

  return type_map.get(type_to_map)
