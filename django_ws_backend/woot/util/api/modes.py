
class Mode():
  def __init__(self, description):
    self.description = description

class Full(Mode):
  value = 3

class Verbose(Mode):
  value = 2

class Normal(Mode):
  value = 1

class Tiny(Mode):
  value = 0

class modes:
  FULL = Full
  VERBOSE = Verbose
  NORMAL = Normal
  TINY = Tiny
