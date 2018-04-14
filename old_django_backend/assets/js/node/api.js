
var _ = require('./util');
var mods = require('./mods');

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
      }).then(function () {
        return _.token;
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
    this.Instance = function (_args) {
      var _instance = this;
      _.map(_args, function (_key, _arg) {
        if (_model.fields.contains(_key)) {
          _instance[_key] = _arg;
        }
      });
    }
    this.Instance.prototype = {
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
      remove: function () {

      },
      bind: function () {

      },
    }
    this.instance = function (_args) {
      return new this.Instance(_args);
    }
    this.objects = {
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
        return _.p().then(function () {
          if (force) {
            return _.request(`${_api.urls.base}${_model.prefix}/${_id}`, 'GET', data).then(function (result) {
              result = _.is.array(result) ? result : [result];
              result.map(function (item) {
                _api.buffer[_model.name][item._id] = item;
                return item;
              });
            });
          }
        }).then(function () {
          // TODO: apply filters

          return _.p(function () {
            return _.map(_api.buffer[_model.name], function (index, item) {
              return _model.instance(item);
            });
          });
        });
      },
    }
  }
  this.models = {};
  this.model = function (args) {
    var _api = this;
    var _model = new this.Model(args);

    // Add to list of models
    _api.models[args.name] = _model;
  }
}

module.exports = new API();
