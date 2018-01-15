var API = function () {
  var _api = this;
  _api.buffer = {};
  _api.active = {};

  _api.token = undefined;
  _api.socket = undefined;
  _api.csrf = document.getElementsByName('csrfmiddlewaretoken')[0].getAttribute('value');
  _api.request = function (url, type, data) {
    type = (type || 'GET');
    return new Promise(function (resolve, reject) {
      var http = new XMLHttpRequest();
      url = type === 'GET' ? `${url}?${_.params(data)}` : url;
      http.open(type, url, true);
      if (_api.token !== undefined) {
        http.setRequestHeader('Authorization', `Token ${_api.token}`);
      }
      http.setRequestHeader('X-CSRFToken', _api.csrf);
      http.setRequestHeader('Content-Type', 'application/json');
      http.onreadystatechange = function () {
        if (http.readyState == 4 && http.status == 200) {
          setTimeout(function () {
            resolve(JSON.parse(http.responseText));
          }, 0); // artificial delay
        }
      }
      http.send(JSON.stringify(data));
    });
  },

  _api.setup = function (args) {
    args = (args || {});
    _api.urls = {
      base: (args.base || '/api/'),
      schema: (args.schema || 'schema/'),
      token: (args.token || 'token/'),
      socket: (args.socket || 'socket/'),
    }

    return _api.request(_api.urls.base + _api.urls.schema).then(function (schema) {
      _api.schema = schema;
      return _.pmap(_api.schema, function (_name, _args) {
        _args['name'] = _name;
        let _model = _api.model(_args);
      });
    }).then(function () {
      return _.all([
        _api.getToken(),
        _api.getSocket(),
      ]);
    });
  }
  _api.getToken = function (username, password) {
    return _api.request(_api.urls.base + _api.urls.token, 'POST', {username: username, password: password}).then(function (result) {
      return _.p(function () {
        _api.token = result.token;
      });
    });
  }
  _api.getSocket = function (username, password) {
    return _api.request(_api.urls.base + _api.urls.socket, 'POST', {username: username, password: password}).then(function (result) {
      return _.p(function () {
        _api.socket = result.socket;
        _api.ws = new WebSocket(`ws://${result.host}:${result.port}`);
        _api.ws.onopen = function () {
          _api.ws.send(_api.socket);
        }
        _api.ws.onmessage = function (event) {
          console.log(event.data);
        }
      });
    });
  }

  _api.Model = function (args) {
    this.name = args.name;
    this.prefix = args.prefix;
    this.basename = args.basename;
    this.fields = args.fields;
    this.fields.push('id');
    var _model = this;

    // model instance
    _model.Instance = function (_args) {
      var _instance = this;
      _instance._model = _model;
      _.map(_args, function (_key, _arg) {
        if (_model.fields.contains(_key)) {
          _instance[_key] = _arg;
          if (_key === '_id') {
            _instance['id'] = _arg;
          }
        }
      });
    }
    _model.Instance.prototype = {
      save: function () {
        var _instance = this;
        return _api.request(`${_api.urls.base}${_model.prefix}/${_instance._id}/`, 'PATCH', _instance);
      },
      get: function () {
        var _instance = this;
        return _api.request(`${_api.urls.base}${_model.prefix}/${_instance._id}/`, 'GET').then(function (item) {
          _api.buffer[_model.name][item._id] = item;
          return item;
        });
      },
      method: function (_method, type, data) {
        var _instance = this;
        return _api.request(`${_api.urls.base}${_model.prefix}/${_instance._id}/${(_method || '')}/`, type, data);
      },
      related: function (property, force) {
        var _instance = this;
        return _.p(function () {
          if (_model.fields.contains(property)) {
            if (_.is.object.all(_instance[property])) {
              return _instance[property];
            } else if (_instance[property].split) {
              var details = _instance[property].split('.');
              if (details.length === 2) {
                var [model, id] = details;
                return _api.get(model, id, force).then(function (_related) {
                  if (_related) {
                    _instance[property] = _related;
                    return _related;
                  }
                });
              }
            }
          }
        });
      },
      many: function (property, force) {
        var _instance = this;
        return _.p(function () {
          if (_model.fields.contains(property) && _.is.array(_instance[property])) {
            return _.all(_instance[property].map(function (_ref, _index) {
              if (_.is.object.all(_ref)) {
                return _ref;
              } else if (_ref.split) {
                var details = _ref.split('.');
                if (details.length === 2) {
                  var [model, id] = details;
                  return _api.get(model, id, force).then(function (_related) {
                    if (_related) {
                      _instance[property][_index] = _related;
                      return _related;
                    }
                  });
                }
              }
            }));
          }
        });
      },
      remove: function () {
        var _instance = this;
        return _api.request(`${_api.urls.base}${_model.prefix}/${_instance._id}/`, 'DELETE');
      },
      bind: function () {
        // used for two-way data binding
      },
      activate: function () {
        var _instance = this;
        return _.p(function () {
          _api.active[_model.name] = _instance;
        });
      },
    }
    _model.instance = function (_args) {
      return new this.Instance(_args);
    }
    _model.objects = {
      get: function (_id, args) {
        args = (args || {});
        if (_.is.object.all(_id)) { // substitute args for _id
          args = _id;
        } else {
          args._id = _id;
        }
        return _model.objects.filter(args).then(function (results) {
          return results.length ? results[0] : undefined;
        });
      },
      method: function (_method, type, data) {
        return _api.request(`${_api.urls.base}${_model.prefix}/${(_method || '')}/`, type, data);
      },
      create: function (data) {
        return _api.request(`${_api.urls.base}${_model.prefix}/`, 'POST', data).then(function (item) {
          return _.p(function () {
            if ('_id' in item) {
              _api.buffer[_model.name] = (_api.buffer[_model.name] || {});
              _api.buffer[_model.name][item._id] = _model.instance(item);
              return _model.instance(item);
            } else {
              _.l(item);
              return undefined;
            }
          });
        });
      },
      all: function (force) {
        return _model.objects.filter({force: force});
      },
      filter: function (args) {
        _api.buffer[_model.name] = (_api.buffer[_model.name] || {});
        args = (args || {});
        var force = (args.force || false);
        var data = (args.data || []); // a list of key-pairs for searching

        /* data is of the form:
        [
          {
            key: 'server query string, e.g. model__name',
            value: 'value',
          },
          ...
        ]

        */

        var path_or_id = (args._id || args.path);
        path_or_id = path_or_id ? `${path_or_id}/` : '';
        return _model.objects.local(args).then(function (instances) {
          if (force || !instances.length) {

            // convert data list into dictionary for request
            var requestData = data.map(function (item, index) {
              let newItem = {};
              if (item.value) {
                newItem[`${index}`] = `${(item.q || 'AND')}-${item.key}-${item.value}`;
              }
              return newItem;
            }).reduce(function (whole, part) {
              return _.merge(whole, part);
            }, {});

            // send request
            return _api.request(`${_api.urls.base}${_model.prefix}/${path_or_id}`, 'GET', requestData).then(function (results) {
              // convert the list of results into instances of the model
              results = _.is.array(results) ? results : [results];
              results.map(function (item) {
                let _instance = _model.instance(item);
                _api.buffer[_model.name][item._id] = _instance;
              });
            }).then(function () {
              return _model.objects.local(args);
            });
          } else {
            return instances;
          }
        });
      },
      local: function (args) {
        args = (args || {});
        return _.pmap(_api.buffer[_model.name], function (_id, _instance) {
          return _instance;
        }).then(function (instances) {
          if (instances) {
            if (args._id) {
              // only compare the id if it's there
              return instances.filter(function (_instance) {
                return _instance._id === args._id;
              });
            } else {
              // get list of properties to compare
              return _.all(instances.map(function (_instance) {

                // args.data is a list of keys and values to compare with nested properties
                // for each instance, the final values of those nested properties need to be returned to be compared
                // this is very inefficient, but for now, it will do
                // especially given the small amount of data going through the system
                return _model.objects.properties(_instance, args).then(function (properties) {
                  return {
                    instance: _instance,
                    properties: properties,
                  };
                });
              })).then(function (instancesAndProperties) {
                return instancesAndProperties.filter(function (_instanceAndProperties) {

                  // filter
                  let _and = _instanceAndProperties.properties.filter(function (_property) {
                    return _property.q === 'AND' || _property.q === undefined;
                  });
                  let _or = _instanceAndProperties.properties.filter(function (_property) {
                    return _property.q === 'OR';
                  });

                  // arrays and boolean values
                  let AND = (!_and.length || _and.every(function (_property) {
                    return _property.value;
                  }));
                  let OR = (!_or.length || _or.some(function (_property) {
                    return _property.value;
                  }));

                  return AND && OR;
                }).map(function (_instanceAndProperties) {
                  return _instanceAndProperties.instance;
                });
              });
            }
          }
        });
      },
      properties: function (_instance, args) {
        args = (args || {data: []});
        args.data = (args.data || []);

        // model__club__name -> ['model', 'club', 'name']
        // model__verbose_name__icontains -> ['model', 'verbose_name', 'icontains']

        // 1. try treating the first item in the query list as a related object.
        // 2.

        return _.all(args.data.map(function (_filter) {
          let _nestedList = (_filter.key || '').split('__');
          let _first = _nestedList.shift();
          let _rest = _nestedList.join('__');

          if (_first) {
            return _instance.related(_first).then(function (_related) {
              if (_related) {
                // model, club__name
                // club, name
                // recursive fetch related properties
                return _related._model.objects.properties(_related, {data: [
                  {
                    key: _rest,
                    value: _filter.value,
                    q: _filter.q,
                  }
                ]}).then(function (properties) {
                  return properties[0];
                });
              } else {

                // maybe matches many instead
                return _instance.many(_first).then(function (many) {
                  if (many) {
                    // iterate through each related objects
                    return _.all(many.map(function (_related) {
                      return _related._model.objects.properties(_related, {data: [
                        {
                          key: _rest,
                          value: _filter.value,
                          q: _filter.q,
                        }
                      ]}).then(function (properties) {
                        return properties[0];
                      });
                    })).then(function (_many) {
                      // needs to be returned as a single list.
                      // will match if any of the many related objects matched.
                      return {q: _filter.q, value: _many.some(function (_property) {
                        return _property.value;
                      })};
                    });
                  } else {
                    // name
                    // name, contains
                    // not a related object, must be a property
                    if (_model.fields.contains(_first)) {
                      if (_rest) {
                        // if _first is not a related object, then _rest must be a modifier, such as "contains".
                        if (_rest == 'contains') {
                          return {q: _filter.q, value: _instance[_first].contains(_filter.value)};
                        } else if (_rest == 'icontains') {
                          return {q: _filter.q, value: (_instance[_first] || '').toLowerCase().contains((_filter.value || '').toLowerCase())};
                        }
                      } else {
                        // simply return the value match
                        return {q: _filter.q, value: _instance[_first] === _filter.value};
                      }
                    } else {
                      return {q: _filter.q, value: false}; // no match
                    }
                  }
                });
              }
            });
          } else {
            return {q: _filter.q, value: true}; // no filter
          }
        }));
      },
    }
  }
  _api.models = {};
  _api.model = function (args) {
    var _model = new this.Model(args);

    // Custom routes
    _.map(args.routes, function (_name, _route) {
      _name = _name.replace(`${_model.basename}-`, '').split('-').join('_');
      if (!['list', 'detail'].contains(_name)) {
        // remove prefix from route
        _route = _route.replace(`${_model.prefix}/`, '').replace('^', '').replace('$', '').split('/');
        if (_route.length == 2) {
          // list_route
          let _url = _route[0];
          _model.objects[_name] = function (data) {
            return _model.objects.filter({force: force, path: _url});
          }
        } else if (_route.length == 4) {
          // detail_route
          let _url = _route[2];
          _model.Instance.prototype[_name] = function (data) {
            var _instance = this;
            return _api.request(`${_api.urls.base}${_model.prefix}/${_instance._id}/${_url}/`, 'POST', (data || {}));
          }
        }
      }
    });

    // Add to list of models
    _api.models[args.name] = _model;
  }

  // shortcuts
  _api.get = function (model, id, force) {
    return _.p(function () {
      if (model in _api.models) {
        return _api.models[model].objects.get(id, force);
      }
    });
  }
}

var api = new API();
