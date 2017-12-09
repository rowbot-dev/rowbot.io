var API = function () {
  var _api = this;
  this.buffer = {};
  this.active = {};

  this.setup = function (args) {
    args = (args || {});
    this.urls = {
      base: (args.base || '/api/'),
      schema: (args.schema || 'schema/'),
      token: (args.token || 'token/'),
    }

    return _.request(this.urls.base + this.urls.schema).then(function (schema) {
      return _.pmap(schema, function (_name, _args) {
        _args['name'] = _name;
        let _model = _api.model(_args);
      });
    });
  }
  this.getToken = function (username, password) {
    return _.request(this.urls.base + this.urls.token, 'POST', {username: username, password: password}).then(function (result) {
      return _.p(function () {
        _.token = result.token;
      });
    });
  }

  this.Model = function (args) {
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
        return _.request(`${_api.urls.base}${_model.prefix}/${_instance._id}/`, 'PATCH', _instance);
      },
      get: function () {
        var _instance = this;
        return _.request(`${_api.urls.base}${_model.prefix}/${_instance._id}/`, 'GET').then(function (item) {
          _api.buffer[_model.name][item._id] = item;
          return item;
        });
      },
      method: function (_method, type, data) {
        var _instance = this;
        return _.request(`${_api.urls.base}${_model.prefix}/${_instance._id}/${(_method || '')}/`, type, data);
      },
      relation: function (property, force) {
        var _instance = this;
        if (_model.fields.contains(property)) {
          var [model, id] = _instance[property].split('.');
          return _api.get(model, id, force);
        }
      },
      remove: function () {

      },
      bind: function () {

      },
    }
    _model.instance = function (_args) {
      return new this.Instance(_args);
    }
    _model.objects = {
      get: function (_id, args) {
        args = (args || {});
        args.id = _id;
        return _model.objects.filter(args).then(function (results) {
          return results.filter(function (item) {
            return item._id === _id;
          });
        }).then(function (results) {
          return results.length ? results[0] : undefined;
        });
      },
      method: function (_method, type, data) {
        return _.request(`${_api.urls.base}${_model.prefix}/${(_method || '')}/`, type, data);
      },
      create: function (data) {
        return _.request(`${_api.urls.base}${_model.prefix}/`, 'POST', data).then(function (item) {
          return _.p(function () {
            if (_id in item) {
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
        var _id = args.id ? `${args.id}/` : '';
        return _model.objects.local().then(function (_models) {
          if (force || !_models.length) {
            return _.request(`${_api.urls.base}${_model.prefix}/${_id}`, 'GET', data).then(function (result) {
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
          if (args.id) {
            return data.filter(function (item) {
              return item._id === args.id;
            })[0];
          } else {
            return data;
          }
        });
      },
      get: function (id, force) {
        return _model.objects.filter({id: id, force: force});
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
  this.models = {};
  this.model = function (args) {
    var _api = this;
    var _model = new this.Model(args);

    // Custom routes. Maybe do later if needed.
    // _.map(args.routes, function (_name, _route) {
    //   _name = _name.replace(`${_model.basename}-`, '').split('-').join('_');
    //   if (!['list', 'detail'].contains(_name)) {
    //     // remove prefix from route
    //     _route = _route.replace(`${_model.prefix}/`, '').replace('^', '').replace('$', '').split('/');
    //     if (_route.length == 2) {
    //       // list_route
    //       let _url = _route[0];
    //       _model.objects[_name] = function (data) {
    //
    //       }
    //     } else if (_route.length == 4) {
    //       // detail_route
    //       let _url = _route[2];
    //       _model.Instance.prototype[_name] = function (data) {
    //
    //       }
    //     }
    //
    //   }
    // });

    // Add to list of models
    _api.models[args.name] = _model;
  }

  this.get = function (model, id, force) {
    var _this = this;
    return _.p(function () {
      if (model in _this.models) {
        return _this.models[model].objects.get(id, force);
      }
    });
  }
}

var api = new API();
