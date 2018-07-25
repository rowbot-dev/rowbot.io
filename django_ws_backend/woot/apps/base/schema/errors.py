
from util.api import Error

class UniformInclusiveError(Error):
  code = '005'
  name = 'uniform_attribute_inclusive'
  description = 'Attribute keys must be all inclusive or exclusive'

class NonNullableNotIncludedError(Error):
  code = '006'
  name = 'non_nullable_not_included'
  description = 'All non-nullable fields must be included'
  description_with_arguments = 'Non-nullable fields [{}] must be included'

  def __init__(self, not_included=None):
    self.description = (
      self.description_with_arguments.format(','.join(not_included))
      if not_included is not None
      else self.description
    )

class MustContainAllNonNullableKeysError(Error):
  code = '007'
  name = 'must_contain_non_nullable'
  description = 'All keys with non-nullable fields must be included'

  def __init__(self, not_included=None):
    self.description = (
      self.description_with_arguments.format(','.join(not_included))
      if not_included is not None
      else self.description
    )

class QueryKeyValueNotPresentError(Error):
  code = '008'
  name = 'query_key_value_not_present'
  description = 'Both key and value must be present'

class QueryAndOrPresentWithKeyValueError(Error):
  code = '009'
  name = 'query_and_or_present_with_key_value'
  description = 'AND and OR keys must not be present with key or value keys'

class QueryAndOrPresentError(Error):
  code = '010'
  name = 'query_and_or_present'
  description = 'A query cannot contain both AND and OR keys'

class FieldDoesNotExistError(Error):
  code = '011'
  name = 'model_field_does_not_exist'
  description = 'The given field must exist on the model'
  description_with_arguments = 'Field <{}> does not exist on the <{}> model'

  def __init__(self, field=None, model=None):
    self.description = (
      self.description_with_arguments.format(field, model)
      if field is not None and model is not None
      else self.description
    )

class MultipleDirectivesForNonRelatedFieldError(Error):
  code = '012'
  name = 'model_multiple_directives'
  description = 'Fields can only respond to a single directive'
  description_with_arguments = 'Multiple directives given for field <{}>: [{}]'

  def __init__(self, field=None, directives=None):
    self.description = (
      self.description_with_arguments.format(field, ','.join(directives))
      if field is not None and directives is not None
      else self.description
    )

class InvalidQueryDirectiveError(Error):
  code = '013'
  name = 'model_invalid_directive'
  description = 'Unrecognised directive'
  description_with_arguments = 'Invalid directive given for field <{}>: <{}>'

  def __init__(self, field=None, directive=None):
    self.description = (
      self.description_with_arguments.format(field, directive)
      if field is not None and directive is not None
      else self.description
    )

class model_schema_errors:
  UNIFORM_INCLUSIVE = UniformInclusiveError
  NON_NULLABLE_NOT_INCLUDED = NonNullableNotIncludedError
  MUST_CONTAIN_ALL_NON_NULLABLE = MustContainAllNonNullableKeysError
  QUERY_KEY_VALUE_NOT_PRESENT = QueryKeyValueNotPresentError
  QUERY_AND_OR_PRESENT_WITH_KEY_VALUE = QueryAndOrPresentWithKeyValueError
  QUERY_AND_OR_PRESENT = QueryAndOrPresentError
  FIELD_DOES_NOT_EXIST = FieldDoesNotExistError
  MULTIPLE_DIRECTIVES_FOR_NON_RELATED_FIELD = MultipleDirectivesForNonRelatedFieldError
  INVALID_QUERY_DIRECTIVE = InvalidQueryDirectiveError
