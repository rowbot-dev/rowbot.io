
from apps.rowbot.models import (
  AssetModel, Asset, AssetInstance,
  Club,
  EventModel, EventNotificationModel, Event, EventInstance, EventNotification,
  Member,
  RoleModel, RolePermission, Role, RoleInstance, RoleRecord,
  TeamModel, Team, TeamInstance, TeamRecord
)

def query(data):

  # data
  # {
  #   'context': {
  #     'socket': '<socket>',
  #     'message': '<message>',
  #     'user': '<user>',
  #     'token': '<token>',
  #   },
  #   'data': {
  #
  #   },
  # }

  # Requests that could be made by the client:
  # 1. Please fetch data that matches these conditions
  # {
  #   'context': {},
  #   'data': {
  #     '<Model>': {
  #       '<function>': {
  #         '<parameter>': '<value>',
  #       },
  #       'fetch': True,
  #       'properties': {
  #         '<property>': True,
  #       },
  #       'limit',
  #       'filter',
  #       'sort',
  #       'pagination',
  #     },
  #   },
  # }

  # Response:
  # {
  #   'context': {},
  #   'data': {
  #     '<Model>': {
  #       'instances': {
  #         '<id>': {
  #           '<property>': '<value>',
  #         },
  #       },
  #       'limit': '<limit>',
  #       'sort': {
  #         '<id>': '<score>',
  #         '<id>': '<score>',
  #         '<id>': '<score>',
  #       },
  #       'pagination': {
  #         'size': '<size>'
  #         'pages': '<pages>',
  #         'page': '<page>',
  #       },
  #     }
  #   }
  # }

  # Errors:
  # {
  #   'context': {},
  #   'data': {},
  #   'errors': {
  #     '<Model>': {
  #       'model': [
  #         {
  #           'code': '001',
  #           'type': 'model_no_model',
  #           'value': 'No such model exists',
  #         }
  #       ],
  #       'functions': {
  #         '<function>': {
  #           '<parameter>': [
  #             {
  #               'code': '002',
  #               'type': 'functions_no_parameter',
  #               'value': 'No such parameter exists'
  #             },
  #             {
  #               'code': '003',
  #               'type': 'functions_missing_parameter',
  #               'value': 'Function parameter missing'
  #             },
  #             {
  #               'code': '004',
  #               'type': 'functions_incorrect_parameter_type',
  #               'value': 'Incorrect parameter type for function'
  #             },
  #           ],
  #         },
  #       },
  #       'properties': {
  #         '<property>': [
  #           {
  #             'code': '005',
  #             'type': 'properties_cannot_be_omitted',
  #             'value': 'Property cannot be omitted',
  #           },
  #           {
  #             'code': '006',
  #             'type': 'properties_no_property',
  #             'value': 'No such property exists',
  #           }
  #         ],
  #       },
  #       'instances': {
  #         '<id>': {
  #           'instance': [
  #             {
  #               'code': '005',
  #               'type': 'instances_no_instance',
  #               'value': 'No such instance exists',
  #             },
  #           ],
  #           'properties': {
  #             '<property>': [
  #               {
  #                 'code': '006',
  #                 'type': 'instances_no_property',
  #                 'value': 'No such property exists',
  #               },
  #             ],
  #           },
  #         },
  #       },
  #       'filter': {
  #         '<filter>': {
  #           '<property>': [
  #             {
  #               'code': '007',
  #               'type': 'filter_cannot_filter',
  #               'value': 'Cannot filter by property',
  #             },
  #           ],
  #         }
  #       },
  #     },
  #   }
  # }

  # 2. Please refresh data that has these references
  # {
  #   'context': {},
  #   'data': {
  #     '<Model>': {
  #       'fetch': True,
  #       'properties': {
  #         '<property>': True,
  #       }
  #       'instances': {
  #         '<id>': {
  #           '<property>': True,
  #         },
  #       }
  #     },
  #   },
  # }

  # Response:
  # {
  #   'context': {},
  #   'data': {
  #     '<Model>': {
  #       'instances': {
  #         '<id>': {
  #           '<property>': '<value>',
  #         },
  #       },
  #     },
  #   },
  # }

  # Errors:
  # {
  #   'context': {},
  #   'data': {},
  #   'errors': {
  #     '<Model>': {
  #       'model': [
  #         {
  #           'code': '001',
  #           'type': 'model_no_model',
  #           'value': 'No such model exists',
  #         }
  #       ],
  #       'properties': {
  #         '<property>': [
  #           {
  #             'code': '006',
  #             'type': 'properties_no_property',
  #             'value': 'No such property exists',
  #           }
  #         ],
  #       },
  #       'instances': {
  #         '<id>': {
  #           'instance': [
  #             {
  #               'code': '005',
  #               'type': 'instances_no_instance',
  #               'value': 'No such instance exists',
  #             },
  #           ],
  #           'properties': {
  #             '<property>': [
  #               {
  #                 'code': '006',
  #                 'type': 'instances_no_property',
  #                 'value': 'No such property exists',
  #               },
  #             ],
  #           },
  #         },
  #       },
  #     },
  #   },
  # }

  # 3. Please create data using these parameters
  # {
  #   'context': {},
  #   'data': {
  #     '<Model>': {
  #       'fetch': True,
  #       'create': {
  #         '<temp_id>': {
  #           '<property>': '<value>',
  #         },
  #       },
  #     },
  #   },
  # }

  # Response: same as (1)

  # Errors:
  # {
  #   'context': {},
  #   'data': {},
  #   'errors': {
  #     '<Model>': {
  #       'model': [
  #         {
  #           'code': '001',
  #           'type': 'model_no_model',
  #           'value': 'No such model exists',
  #         }
  #       ],
  #       'create': {
  #         '<temp_id>': {
  #           '<property>': [
  #             {
  #               'code': '006',
  #               'type': 'instances_no_property',
  #               'value': 'No such property exists',
  #             },
  #           ],
  #         },
  #       },
  #     },
  #   },
  # }

  # 4. Please delete data that has these references
  # {
  #   'context': {},
  #   'data': {
  #     '<Model>': {
  #       'delete': [
  #         '<id>',
  #       ],
  #     },
  #   },
  # }

  # Response:
  # {
  #   'context': {},
  #   'data': {
  #     '<Model>': {
  #       'delete': [
  #         '<id>',
  #       ],
  #     },
  #   },
  # }

  # Errors:
  # {
  #   'context': {},
  #   'data': {},
  #   'errors': {
  #     '<Model>': {
  #       'model': [
  #         {
  #           'code': '001',
  #           'type': 'model_no_model',
  #           'value': 'No such model exists',
  #         }
  #       ],
  #       'delete': {
  #         '<id>': [
  #           {
  #             'code': '005',
  #             'type': 'instances_no_instance',
  #             'value': 'No such instance exists',
  #           },
  #         ],
  #       },
  #     },
  #   }
  # }

  # 5. Please sort/filter/paginate these data that have these references according to these parameters
  # {
  #   'context': {},
  #   'data': {
  #     '<Model>': {
  #       'fetch': False,
  #       'instances': [
  #         '<id>',
  #       ],
  #       'filter': {
  #         '<property__relationship>': '<value>',
  #       },
  #       'sort': {
  #         '<property__relationship>': '<value>',
  #       },
  #       'pagination': {
  #         'size': 10,
  #         'page': 14,
  #       },
  #     },
  #   },
  # }

  # Response: same as (1)

  # Errors: same as (1)


  # Server messages: things that can be triggered by the server only

  # 1. Schema:
  # 2. Notifications:
  # 3. Errors:
  # 4. Authentication challenge:

  pass
