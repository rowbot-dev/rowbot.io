var UI = function () {

  // component object
  this.Component = function (name) {
    this.name = name;
    this._ = {
      children: {
        buffer: [],
        rendered: [],
        index: {},
      },
      states: [],
      before: undefined,
      root: undefined,
      is: {
        rendered: false,
      },
      style: {},
      properties: {},
      classes: [],
    };
  }
  this.Component.prototype = {
    hook: document.getElementById('hook'),
    init: function (args) {
      let _this = this;
      _this._.before = args.before;
      _this._.root = args.root;
      _this._.tag = (args.tag || 'div');
      return _.all([
        _this.setStyle(args.style),
        _this.setClasses(args.classes),
        _this.setProperties(args.properties),
        _this.setStates(args.states),
        _this.setBindings(args.bindings),
        _this.setChildren(args.children),
      ]).then(function () {
        return _this;
      });
    },

    // pre-render or post-render
    setStyle: function (style, duration) {
      var _this = this;
      style = (style || {});
      duration = (duration || 0);
      style = _.merge(style, {'': {}}); // make buffer for self style
      _.map(style, function (key, value) {
        if (!_.is.object.all(value)) {
          delete style[key];
          style[''][key] = value;
        }
      });

      // update style dictionary
      // var _original = _this._.style[''];
      _this._.style = _.merge(_this._.style, style);

      // add styles to DOM if rendered
      if (_this._.is.rendered) {
        var element = _this.element();
        return _.pmap(_this._.style, function (key, _style) {
          // TODO: allow nested styles for active, etc.
          // This sets up a new css rule with a string reduced from the style object
          if (key) {
            return _.css.create(`${_this._.tag}#${_this.id} ${key}`, _.map(_style, function (_key, _value) {
              return `${_key}: ${_value};`;
            }).reduce(function (whole, part) {
              return `${whole}\n${part}`;
            }, '').trim());
          } else {
            if (duration) {
              return $(element).animate(_this._.style[''], {duration: duration}).promise();
            } else {
              return _.pmap(_style, function (key, value) {
                return _.p(function () {
                  element.style[key] = value;
                });
              });
            }
          }
        });
      }
    },
    setClasses: function (classes) {
      var _this = this;
      classes = (classes || []);
      _this._.classes = _.map(_.merge(_this._.classes, classes), function (index, value) {
        return value;
      });

      if (_this._.is.rendered) {
        var element = _this.element();
        return _.all(_this._.classes.map(function (className) {
          return _.p(function () {
            element.classList.add(className);
          });
        }));
      }
    },
    setProperties: function (properties) {
      var _this = this;
      properties = (properties || {});
      _this._.properties = _.merge(_this._.properties, properties);

      if (_this._.is.rendered) {
        var element = _this.element();
        return _.pmap(_this._.properties, function (key, property) {
          return _.p(function () {
            element.setAttribute(key, property);
          });
        });
      }
    },
    setBindings: function (bindings) {
      var _this = this;
      bindings = (bindings || {});
      _this._.bindings = _.merge(_this._.bindings, bindings);

      if (_this._.is.rendered) {
        var element = _this.element();
        return _.pmap(_this._.bindings, function (key, binding) {
          return _.p(function () {
            element.addEventListener(key, function (event) {
              if (event.target.id == _this.id) {
                return binding(_this, event);
              }
            });
          });
        });
      }
    },
    setStates: function (states) {
      let _this = this;
      states = (states || []);
      return _.all(states.map(function (unresolved) {
        return _.p(unresolved).then(function (state) {
          _this._.states.push(state);
          return state.register(_this);
        });
      }));
    },
    setChildren: function (children) {
      let _this = this;
      children = (children || _this._.children.buffer);
      return _._all(children.map(function (unresolved) {
        return function () {
          return _.p(unresolved).then(function (child) {
            if (_this._.is.rendered) {
              return _this.renderChild(child);
            } else {
              return _this.bufferChild(child);
            }
          });
        }
      }));
    },
    renderChild: function (child) {
      // root, before, indices
      var _this = this;
      return child.render().then(function () {
        // remove recently rendered child from buffer
        return _.p(function () {
          _this._.children.buffer.shift();
        });
      }).then(function () {
        // insert the child into the correct place in the rendered array
        // 1. in order to know index, I need to know the index of the thing before it.
        // 2. if the array is currently empty, its index is 0.
        return _.p(function () {
          var index = child._.before === undefined ? _this._.children.rendered.length : _this._.children.index[child._.before];
          _this._.children.rendered.splice(index, 0, child);
          _this._.children.rendered.forEach(function (rendered, index) {
            _this._.children.index[rendered.name] = index;
          });
        });
      }).then(function () {
        return child;
      });
    },
    bufferChild: function (child) {
      var _this = this;
      return _.p(function () {
        child._.parent = _this;
        _this._.children.buffer.push(child);
      });
    },

    // post-render
    removeClass: function (classes) {

    },
    removeProperty: function (properties) {

    },

    // element
    element: function () {
      var _this = this;
      if (!_this._.is.rendered) {
        var element = document.createElement(_this._.tag);
        element.id = _this.id;
        return element;
      } else {
        return document.getElementById(_this.id);
      }
    },

    // render
    setID: function () {
      var _this = this;
      return _.p(function () {
        var parentID = (_this._.parent || {}).id;
        _this.id = `${(parentID || '')}${(parentID ? '-' : '')}${_this.name}`;
        return _this.id;
      });
    },
    render: function (root) {
      var _this = this;
      return _this.setID().then(function () {
        // 1. actually render to DOM
        var element = _this.element();
        var root = _this._.parent !== undefined ? _this._.parent.element() : _this.hook;
        var before = _this._.before !== undefined ? _this._.parent.child(_this._.before) : undefined;
        if (before !== undefined) {
          var beforeElement = before.element();
          root.insertBefore(element, beforeElement);
        } else {
          root.appendChild(element);
        }

        // 2. write styles to DOM
        _this._.is.rendered = true;
        return _.all([
          _this.setStyle(),
          _this.setClasses(),
          _this.setProperties(),
          _this.setBindings(),
        ]).then(function () {
          // 3. go down through children
          return _this.setChildren();
        });
      });
    },

    // tree
    child: function (name) {
      // supports indices
      var _this = this;
      var _buffer = _this._.is.rendered ? _this._.children.rendered : _this._.children.buffer;
      return _buffer.filter(function (child, index) {
        return _.is.number(name) ? index === name : child.name === name;
      })[0];
    },
    get: function (path) {
      // flawless
      // supports: dot sep string, string array, integer array
      // with the caveat that, until rendering, the index will refer to the order in the definition.
      var names = _.is.array(path) ? path : path.split('.');
      var name = names.shift();
      var newPath = _.is.array(path) ? names : names.join('.');
      var child = this.child(name);
      return newPath && newPath.length && child !== undefined ? child.get(newPath) : child;
    },
  }
  this._component = function (name, args) {
    let _component = new this.Component(name);
    return _component.init(args);
  }

  // state object
  this.State = function (name) {
    this.name = name;
    this._ = {
      children: {
        buffer: {},
        registered: {},
      },
      style: {},
      properties: {},
      classes: [],
      registered: false,
    }
  }
  this.State.prototype = {
    init: function (args) {
      let _this = this;
      _this._.fn = args.fn;
      _this._.duration = args.duration;
      return _.all([
        _this.setStyle(args.style),
        _this.setClasses(args.classes),
        _this.setProperties(args.properties),
        _this.setChildren(args.children),
      ]).then(function () {
        return _this;
      });
    },

    setStyle: function (style) {
      var _this = this;
      style = (style || {});
      style = _.merge(style, {'': {}}); // make buffer for self style
      _.map(style, function (key, value) {
        if (!_.is.object.all(value)) {
          delete style[key];
          style[''][key] = value;
        }
      });

      // update style dictionary
      _this._.style = _.merge(_this._.style, style);
    },
    setClasses: function (classes) {
      var _this = this;
      classes = (classes || []);
      _this._.classes = _.map(_.merge(_this._.classes, classes), function (index, value) {
        return value;
      });
    },
    setProperties: function (properties) {
      var _this = this;
      properties = (properties || {});
      _this._.properties = _.merge(_this._.properties, properties);
    },
    setChildren: function (children) {
      let _this = this;
      children = (children || _.map(_this._.children.buffer, function (key, child) {
        return child;
      }));
      return _.all(children.map(function (unresolved) {
        return _.p(unresolved).then(function (child) {
          if (_this._.registered) {
            return _this.registerChild(child);
          } else {
            return _this.bufferChild(child);
          }
        });
      }));
    },
    bufferChild: function (child) {
      var _this = this;
      return _.p(function () {
        child._.parent = _this;
        _this._.children.buffer[child.name] = child;
      });
    },
    registerChild: function (child) {
      var _this = this;
      return child.register(_this._.component).then(function () {
        return _.p(function () {
          delete _this._.children.buffer[child.name];
          _this._.children.registered[child.name] = child;
        });
      }).then(function () {
        return child;
      });
    },

    // register
    register: function (component) {
      let _this = this;
      _this._.component = component;
      _this._.registered = true;
      return ui.states.register(_this).then(function () {
        return _this.setChildren();
      });
    },

    // tree
    path: function () {
      var _this = this;
      return _this._.parent !== undefined ? `${_this._.parent.path()}.${_this.name}` : _this.name;
    },
    child: function (name) {
      // supports indices
      return this.children[name];
    },
    get: function (path) {
      // flawless
      // supports: dot sep string, string array, integer array
      // with the caveat that, until rendering, the index will refer to the order in the definition.
      var names = _.is.array(path) ? path : path.split('.');
      var name = names.shift();
      var newPath = _.is.array(path) ? names : names.join('.');
      var child = this.child(name);
      return newPath && newPath.length && child !== undefined ? child.get(newPath) : child;
    },

    // activate
    ancestry: function () {
      var _this = this;
      var data = {
        style: _this._.style,
        classes: _this._.classes,
        properties: _this._.properties,
        fn: _this._.fn,
        duration: _this._.duration,
      }
      return _this._.parent !== undefined ? _.merge(_this._.parent.ancestry(), data) : data;
    },
    call: function (durationOverride) {
      var _this = this;
      return _.p(function () {
        var _data = _this.ancestry();
        var _component = _this._.component;
        var _before = ((_data.fn || {}).before || _.p);
        var _after = ((_data.fn || {}).after || _.p);
        var _style = (_data.style || {});
        var _classes = (_data.classes || {});
        var _properties = (_data.properties || {});
        var _duration = durationOverride !== undefined ? durationOverride : (_data.duration || 300);

        // concatenate styles and classes from parent chain
        // execute before and after functions
        return _before(_component).then(function (_result) {
          return _.all([
            _component.setStyle(_style, _duration),
            _component.setClasses(_classes),
            _component.setProperties(_properties),
          ]);
        }).then(function () {
          return _after(_component);
        });
      });
    },
  }
  this._state = function (name, args) {
    var _state = new this.State(name);
    return _state.init(args);
  }

  // state buffer
  this.StateBuffer = function () {
    // TODO: add state map maybe
    this.active = undefined;
    this.buffer = {};
    this.get = function (path) {
      var _this = this;
      return _.p(function () {
        var path_array = path.split('.');
        sub = _this.buffer;
        var i;
        for (i=0; i<path_array.length; i++) {
          if (path_array[i] in sub) {
            sub = sub[path_array[i]];
          } else {
            break;
          }
        }
        return sub['_'];
      });
    }
    this.call = function (path, durationOverride) {
      this.active = path;
      return this.get(path).then(function (states) {
        return _.all(states.map(function (state) {
          return state.call(durationOverride);
        }));
      });
    }
    this.set = function (path, state) {
      var _this = this;
      return _.p(function () {
        var path_array = path.split('.');
        sub = _this.buffer;
        var i;
        for (i=0; i<path_array.length; i++) {
          if (!(path_array[i] in sub)) {
            sub[path_array[i]] = {_: []};
          }
          sub = sub[path_array[i]];

          if (i+1 === path_array.length) {
            sub['_'].push(state);
          }
        }
      });
    }
    this.register = function (state) {
      return this.set(state.path(), state);
    }
  }
  this.states = new this.StateBuffer(),

  // actions
  this.Action = function () {

  }

  // context
  this.API = function () {
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
        }
      }
      this.instance = function (_args) {
        return new this.Instance(_args);
      }
      this.objects = {
        get: function (_id, args) {
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
          return _.p().then(function () {
            if (force) {
              return _.request(`${_api.urls.base}${_model.prefix}/`, 'GET', data).then(function (result) {
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
  }
  this.api = new this.API();
}

var ui = new UI();
