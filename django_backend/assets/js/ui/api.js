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
          resolve(JSON.parse(http.responseText));
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
      return _.pmap(schema, function (_name, _args) {
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
    var _model = this;

    // model instance
    _model.Instance = function (_args) {
      var _instance = this;
      _.map(_args, function (_key, _arg) {
        if (_model.fields.contains(_key)) {
          if (_.is.array(_arg) && _arg.length && _.is.object.all(_arg[0])) {
            var relatedModel = _arg[0]._ref.split('.')[0];
            _instance[_key] = _arg.map(function (_item) {
              return _api.models[relatedModel].instance(_item);
            });
          } else {
            _instance[_key] = _arg;
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
      relation: function (property, force) {
        var _instance = this;
        if (_model.fields.contains(property)) {
          var [model, id] = _instance[property].split('.');
          return _api.get(model, id, force);
        }
      },
      remove: function () {
        var _instance = this;
        return _api.request(`${_api.urls.base}${_model.prefix}/${_instance._id}/`, 'DELETE');
      },
      bind: function () {
        // used for two-way data binding
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
          args.id = _id;
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
              _api.buffer[_model.name][item._id] = item;
              return _model.instance(item);
            } else {
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
        var data = (args.data || {});
        var path_or_id = (args.id || args.path);
        path_or_id = path_or_id ? `${path_or_id}/` : '';
        return _model.objects.local().then(function (_models) {
          if (force || !_models.length) {
            return _api.request(`${_api.urls.base}${_model.prefix}/${path_or_id}`, 'GET', data).then(function (result) {
              result = _.is.array(result) ? result : [result];
              result.map(function (item) {
                var instance = _model.instance(item)
                _api.buffer[_model.name][item._id] = instance;
                return instance;
              });
            });
          }
        }).then(function () {
          return _model.objects.local();
        }).then(function (data) {
          return data.filter(function (item) {
            return Object.keys(args).reduce(function (whole, part) {
              return whole && args[part] === item[part];
            }, true);
          });
        });
      },
      local: function () {
        return _.p(function () {
          return _.map(_api.buffer[_model.name], function (index, item) {
            return item;
          });
        });
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

  _api.get = function (model, id, force) {
    return _.p(function () {
      if (model in _api.models) {
        return _api.models[model].objects.get(id, force);
      }
    });
  }
}

var api = new API();
