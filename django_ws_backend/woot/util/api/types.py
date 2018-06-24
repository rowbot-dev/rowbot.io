
class Type():
  def __init__(self, description=None):
    self.description = description

  def validate(self, value):
    return False

  def render(self):
    return self._type

  @classmethod
  def test(cls, type):
    return type._type == cls._type

class Boolean(Type):
  _type = '__boolean'

  def validate(self, value):
    return isinstance(value, bool)

class Model(Type):
  pass

class Structure(Type):
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
  pass

class UUID(Type):
  pass

class Time(Type):
  pass

class Ref(Type):
  pass

class Enum(Type):
  def __init__(self, *options):
    self.options = options

class Immutable(Type):
  pass

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

  def as_entries():
    pass
