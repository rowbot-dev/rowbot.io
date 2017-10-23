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

      // add styles to DOM if rendered
      if (_this._.is.rendered) {
        return _.pmap(_this._.style, function (key, _style) {

          // TODO: allow nested styles for active, etc.
          key = `${key ? '' : _this._.tag}#${_this.id} ${key}`.trim();

          // This sets up a new css rule with a string reduced from the style object
          return _.css.create(key, _.map(_style, function (_key, _value) {
            return `${_key}: ${_value};`;
          }).reduce(function (whole, part) {
            return `${whole}\n${part}`;
          }, '').trim());
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
            document.addEventListener(key, function (event) {
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
      return _this.setChildren();
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
  }
  this._state = function (name, args) {
    var _state = new this.State(name);
    return _state.init(args);
  }

  // state buffer
  this.StateBuffer = function () {
    this.buffer = {};
    this.get = function (path) {

    }
    this.set = function (path, state) {

    }
  }
  this.states = new this.StateBuffer(),
  // TODO: actually call a state
  // TODO: have a state apply stuff
  // TODO: state maps
  // TODO: call nested states? How to apply? Vary animation time?
  // TODO: Animation method, look up jQuery method

  // keyboard bindings

  // actions
  this.Action = function () {

  }

  // context
  this.Context = function () {

  }
  this.Context.prototype = {

  }
}

var ui = new UI();
