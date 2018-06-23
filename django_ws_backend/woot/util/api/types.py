
class Type():
  def __init__(self, description):
    self.description = description

  def validate(self, value):
    return False

class Boolean(Type):
  def validate(self):
    return False

class Model(Type):
  def validate(self):
    return False

class Structure(Type):
  def validate(self):
    return False

class Array(Type):
  def validate(self):
    return False

class Integer(Type):
  def validate(self):
    return False

class Float(Type):
  def validate(self):
    return False

class String(Type):
  def validate(self):
    return False

class UUID(Type):
  def validate(self):
    return False

class Time(Type):
  def validate(self):
    return False

class Ref(Type):
  def validate(self):
    return False

class Enum(Type):
  def __init__(self, *options):
    self.options = options

  def validate(self):
    return False

class Immutable(Type):
  def validate(self):
    return False

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
