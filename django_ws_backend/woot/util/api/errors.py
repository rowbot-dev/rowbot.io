
class Error():
  pass

class Errors():
  def no_such_model_method(model_name, method_name):
    return 'No such method "{}" for the model "{}"'.format(model_name, method_name)

  def no_such_model(model_name):
    return 'No such model "{}"'.format(model_name)
