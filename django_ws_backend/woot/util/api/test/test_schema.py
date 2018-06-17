
import json
from django.test import TestCase
from util.api.schema import Schema, modes

class EmptyPayloadSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = Schema({}, {}, None, mode=modes.FULL)

  def test_get_context(self):
    self.assertEqual(self.schema.mode, modes.FULL)
    self.assertEqual(self.schema.authorization, None)

  def test_render_for_payload_check(self):
    self.schema.render_for_payload_check()
    self.assertEqual(self.schema.payload_check_render, {
      'context': {
        '_description': 'The context of the request or response contains query-specific identifiers such as UUIDs, timestamps, and hashes.',
        'mode': {
          '_description': 'The level of detail in the schema',
          '_type': '__string',
          '_values': {
            'full': 'Returns this entire schema including the top-level info key and all description keys, even if the keys are not relevant to the current request or response.',
            'verbose': 'Keeps the description keys, but not the info keys.',
            'normal': 'Removes all description keys and keys not relevant to the request, and moves keys inside request or response to the top level.',
            'tiny': 'Removes all structure including the context when possible. This should only be used to return simple information such as a single value when the endpoint of the response is known.'
          }
        },
        'authorization': {
          '_description': 'An authorization token to be included with each request. It is the primary key of an authorization token object on the system.',
          '_type': '__uuid'
        }
      },
      'query': {
        '_description': 'All queries made to the API must be of this form. Only keys relevant to the query should be included. Any request that does not contain a valid subset of this structure will be rejected with an explicit error.',
        'time': {
          '_description': 'The timestamp of the request from the client side',
          'location': {
            '_description': 'The location of the sender',
            '_type': '__string'
          },
          'locale': {
            '_description': 'The locale of the sender',
            '_type': '__string'
          },
          'timestamp': {
            '_description': 'The time the request left the client',
            '_type': '__time'
          }
        },
        'system': {
          '_description': 'A set of information about the system that the server is running, including version information.',
          '_type': {
            '__boolean': 'Include all system information',
            '__structure': 'Pick system information to include'
          },
          'id': {
            '_description': 'The uuid of the API',
            '_type': '__boolean'
          },
          'name': {
            '_description': 'The name of the API',
            '_type': '__boolean'
          },
          'verboseName': {
            '_description': 'The verbose name of the API',
            '_type': '__boolean'
          },
          'apiVersion': {
            '_description': 'The API version of the API',
            '_type': '__boolean'
          },
          'releaseHash': {
            '_description': 'The release hash of the API',
            '_type': '__boolean'
          },
          'models': {
            '_description': 'System models reserved for key functions such as authentication',
            '_type': {
              '__boolean': 'Include all system models',
              '__structure': 'Pick system models to include'
            },
            'reference': {
              '_description': 'A combination of object name and UUID allowing a reference to a single object on the system',
              '_type': '__boolean'
            },
            'user': {
              '_description': 'A unique identity on the system',
              '_type': '__boolean'
            },
            'authentication': {
              '_description': 'A model used to mediate the authentication process',
              '_type': '__boolean'
            },
            'authorization': {
              '_description': 'An authorization token for persistent access control',
              '_type': '__boolean'
            },
            'error': {
              '_description': 'An error reporting model',
              '_type': '__boolean'
            }
          }
        },
        'models': {
          '_description': 'A list of models available on the system',
          '_template': {
            '_key': '__model',
            'attributes': {
              '_description': 'Non-related object properties of an object. Types and values will be set from the system. During any request, the specified attributes will be included with the response.',
              '_type': {
                '__boolean': 'Include all attributes',
                '__structure': 'Pick attributes to include'
              },
              '_template': {
                '_type': '__boolean'
              }
            },
            'relationships': {
              '_description': 'Related objects referenced via models on the system.',
              '_template': {
                '_type': {
                  '__boolean': 'Include the reference to the object if it is singular, else the related model name.',
                  '__structure': 'Add a level of recursion starting from the models _template.'
                }
              }
            },
            'methods': {
              '_description': 'A list of models available on the system',
              '_template': {
                '_type': {
                  '__boolean': 'Include details of the method',
                  '__structure': 'Call the method with arguments defined by the system'
                }
              }
            },
            'instances': {
              '_description': 'Instances of the model class. Attributes or relationships to include cannot be specified here.',
              '_template': {
                '_key': '__uuid',
                'update': {
                  '_description': 'Set this key to explicitly update the instance rather than fetching it',
                  '_type': '__boolean'
                },
                'attributes': {},
                'methods': {
                  '_description': 'Call methods on a single instance',
                  '_template': {
                    '_type': '__structure'
                  }
                },
                'relationships': {
                  '_template': {
                    '_type': {
                      '__ref': 'Set a singular relationship',
                      '__array': 'Set multiple related objects'
                    }
                  }
                }
              }
            },
            'filter': {
              '_description': 'Impose a filter on a model',
              '_template': {
                '_description': 'An object containing the information necessary to compose a filter',
                'composite': {
                  '_description': 'A string of the form A & B | C, or any combination of unitary operators to combine the named components, conforming to Django query notation.',
                  '_type': '__string'
                },
                'components': {
                  '_description': 'A series of named components in the form related__attributed__directive, conforming to Django query notation.',
                  '_template': {
                    '_type': '__string'
                  }
                }
              }
            },
            'sort': {
              '_description': 'Sort instances of a model',
              '_template': {
                '_description': 'A string of the form (-)relationship__attribute conforming to Django query notation.',
                '_type': '__string'
              }
            },
            'paginate': {
              '_description': 'Paginate instances of a model',
              'page': {
                '_description': 'The current page',
                '_type': {
                  '__boolean': 'Fetch the current value',
                  '__number': 'Set the current value'
                }
              },
              'pages': {
                '_description': 'The current number of pages',
                '_type': '__boolean'
              },
              'size': {
                '_description': 'The current page size',
                '_type': {
                  '__boolean': 'Fetch the current page size',
                  '__number': 'Set the current page size'
                }
              }
            },
            'create': {
              '_description': 'Create instances',
              '_template': {
                '_description': 'Keys will be the identifier of the new instance',
                '_key': '__uuid',
                'identifier': {
                  '_description': 'Each prototype is given a temporary identifier to match it with the newly created object',
                  '_type': '__uuid'
                },
                'attributes': {},
                'relationships': {
                  '_template': {
                    '_type': {
                      '__ref': 'A singular related object',
                      '__array': 'Multiple related objects'
                    }
                  }
                }
              }
            },
            'delete': {
              '_description': 'Delete instances',
              '_template': {
                '_type': '__uuid'
              }
            }
          }
        }
      }
    })

class RecursiveDataCheckTestCase(TestCase):
  def setUp(self):


  def test_simple_object(self):
