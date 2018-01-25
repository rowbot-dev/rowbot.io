
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
      html: undefined,
    };
  }
  this.Component.prototype = {
    hook: document.getElementById('hook'),
    init: function (args) {
      args = (args || {});
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
        _this.setHTML(args.html),
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
      var _changed = _.changed(_this._.style[''], style['']);
      _this._.style = _.merge(_this._.style, style);

      // add styles to DOM if rendered
      if (_this._.is.rendered) {
        var _element = _this.element();
        return _.pmap(_this._.style, function (key, _style) {
          // TODO: allow nested styles for active, etc.
          // This sets up a new css rule with a string reduced from the style object
          if (key) {
            return _.css.create(`${_this._.tag}#${_this.id}${key}`, _.map(_style, function (_key, _value) {
              return `${_key}: ${_value} !important;`;
            }).reduce(function (whole, part) {
              return `${whole}\n${part}`;
            }, '').trim());
          } else {
            if (duration) {
              return $(_element).animate(_changed, {duration: duration}).promise();
            } else {
              return $(_element).css(_style, {queue: false}).promise();
            }
          }
        });
      }
    },
    setClasses: function (classes) {
      var _this = this;
      classes = (classes || []);
      classes = _.is.array(classes) ? classes : [classes];
      _this._.classes = _.map(_.merge(_this._.classes, classes), function (index, value) {
        return value;
      });

      if (_this._.is.rendered) {
        var _element = _this.element();
        return _.all(_this._.classes.map(function (_class) {
          return $(_element).addClass(_class).promise();
        }));
      }
    },
    setProperties: function (properties) {
      var _this = this;
      properties = (properties || {});
      _this._.properties = _.merge(_this._.properties, properties);

      if (_this._.is.rendered) {
        var _element = _this.element();
        return _.pmap(_this._.properties, function (key, property) {
          return $(_element).attr(key, property).promise();
        });
      }
    },
    setBindings: function (bindings) {
      var _this = this;
      bindings = (bindings || {});
      _this._.bindings = _.merge(_this._.bindings, bindings);

      if (_this._.is.rendered) {
        var _element = _this.element();
        return _.pmap(_this._.bindings, function (key, binding) {
          return $(_element).on(key, function (event) {
            return binding(_this, event);
          }).promise();
        });
      }
    },
    setStates: function (states) {
      var _this = this;
      states = (states || []);
      return _.all(states.map(function (unresolved) {
        return _.p(unresolved).then(function (state) {
          _this._.states.push(state);
          return state.register(_this);
        });
      }));
    },
    setChildren: function (children) {
      var _this = this;
      children = (children || _this._.children.buffer);
      children = _.is.array(children) ? children : [children];
      return _._all(children.map(function (unresolved) {
        return function () {
          return _.p(unresolved).then(function (_child) {
            _child._.parent = _this;
            if (_this._.is.rendered) {
              return _this.renderChild(_child);
            } else {
              return _this.bufferChild(_child);
            }
          });
        }
      })).then(function () {
        return _this;
      });
    },
    setHTML: function (html) {
      var _this = this;
      _this._.html = html !== undefined ? html : _this._.html;
      return _.p(function () {
        if (_this._.html !== undefined && _this._.is.rendered) {
          return $(_this.element()).html(_this._.html).promise();
        }
      });
    },
    renderChild: function (_child) {
      // root, before, indices
      var _this = this;
      return _child.render().then(function () {
        // remove recently rendered child from buffer
        return _.p(function () {
          _this._.children.buffer.shift();
        });
      }).then(function () {
        // insert the child into the correct place in the rendered array
        // 1. in order to know index, I need to know the index of the thing before it.
        // 2. if the array is currently empty, its index is 0.
        return _.p(function () {
          var _index = _child._.before === undefined ? _this._.children.rendered.length : _this._.children.index[_child._.before];
          _this._.children.rendered.splice(_index, 0, _child);
          _this._.children.rendered.forEach(function (_rendered, _index) {
            _this._.children.index[_rendered.name] = _index;
          });
        });
      }).then(function () {
        return _child;
      });
    },
    bufferChild: function (_child) {
      var _this = this;
      return _.p(function () {
        _this._.children.buffer.push(_child);
      });
    },
    children: function () {
      let _this = this;
      if (_this._.is.rendered) {
        return _this._.children.rendered;
      } else {
        return _this._.children.buffer;
      }
    },

    // post-render
    removeClass: function (_class) {
      var _this = this;
      if (_class !== undefined) {
        _this._.classes = _this._.classes.filter(function (_cls) {
          return _cls !== _class; // remove from list
        });

        if (_this._.is.rendered) {
          var element = _this.element();
          return $(element).removeClass(_class).promise();
        }
      }
    },
    removeClasses: function (classes) {
      var _this = this;
      return _.all(classes.map(function (_class) {
        return _this.removeClass(_class);
      }));
    },
    removeProperty: function (properties) {

    },
    removeBinding: function (key) {
      var _this = this;
      delete _this._.bindings[key];

      if (_this._.is.rendered) {
        var element = _this.element();
        return $(element).off(key).promise();
      }
    },
    removeChild: function (name) {
      var _this = this;
      return _.p(function () {
        if (_this._.is.rendered) {
          var _child = _this.get(name);
          _this.element().removeChild(_child.element());
          _this._.children.buffer = _this._.children.buffer.filter(function (_any) {
            return _any.name !== _child.name;
          });
        }
      });
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
        var _element = _this.element();
        var root = _this._.parent !== undefined ? _this._.parent.element() : _this.hook;
        var before = _this._.before !== undefined ? _this._.parent.child(_this._.before) : undefined;
        if (before !== undefined) {
          var beforeElement = before.element();
          root.insertBefore(_element, beforeElement);
        } else {
          root.appendChild(_element);
        }

        _this._.is.rendered = true;
        return _.all([
          _this.setStyle(),
          _this.setClasses(),
          _this.setProperties(),
          _this.setBindings(),
          _this.setHTML(),
        ]).then(function () {
          return _this.setChildren();
        });
      });
    },
    hide: function (args) {
      args = (args || {});
      args.style = _.merge({'opacity': '0.0'}, args.style);
      args.duration = args.duration !== undefined ? args.duration : 300;
      var _this = this;
      return _this.setStyle(args.style, args.duration).then(function () {
        return _this.setClasses('hidden');
      });
    },
    show: function (args) {
      args = (args || {});
      args.style = _.merge({'opacity': '1.0'}, args.style);
      args.duration = args.duration !== undefined ? args.duration : 300;
      var _this = this;
      return _this.removeClass('hidden').then(function () {
        return _this.setStyle(args.style, args.duration);
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
      var names = _.is.array(path) ? path : (path || '').split('.');
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
      _this._.fn = (args.fn || {});
      _this._.fn.before = (_this._.fn.before || _.p);
      _this._.fn.animate = (_this._.fn.animate || _.p);
      _this._.fn.after = (_this._.fn.after || _.p);
      _this._.duration = args.duration;
      return _this.setChildren(args.children).then(function () {
        return _this;
      });
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
    get: function (_path) {
      // flawless
      // supports: dot sep string, string array, integer array
      // with the caveat that, until rendering, the index will refer to the order in the definition.
      var names = _.is.array(_path) ? _path : _path.split('.');
      var _name = names.shift();
      var _newPath = _.is.array(_path) ? names : names.join('.');
      var _child = this.child(_name);
      return newPath && _newPath.length && _child !== undefined ? _child.get(_newPath) : _child;
    },
    fetch: function (_path) {
      // merge child properties with current
      var _this = this;
      var fn = {
        component: _this._.component,
        before: _this._.fn.before,
        animate: _this._.fn.animate,
        after: _this._.fn.after,
      }
      return _.p(function () {
        if (_path) {
          var tokens = _path.split('.');
          var _name = tokens.shift();
          var _rest = tokens.join('.');
          var _child = _this.get(_name);

          // return
          return _.merge(fn, _child.fetch(_rest));
        } else {
          return fn;
        }
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
    var _buffer = this;
    _buffer.active = undefined;
    _buffer.buffer = {};
    _buffer.call = function (_path, _duration) {
      // Needs to return the list of top level states matching the first part of the path.
      // Each state will then be triggered using the rest of the path.
      _buffer.active = _path;
      var tokens = _path.split('.');
      var _name = tokens.shift();
      var _rest = tokens.join('.');

      return _.all((_buffer.buffer[_name] || []).map(function (_state) {
        return _state.fetch(_rest);
      })).then(function (fns) {
        return _.all(fns.map(function (_fn) {
          return _fn.before(_fn.component);
        })).then(function () {
          return _.all(fns.map(function (_fn) {
            return _fn.animate(_fn.component, _duration);
          }));
        }).then(function () {
          return _.all(fns.map(function (_fn) {
            return _fn.after(_fn.component);
          }));
        });
      });
    }
    _buffer.register = function (_state) {
      return _.p(function () {
        if (!_state._.parent) {
          _buffer.buffer[_state.name] = (_buffer.buffer[_state.name] || []);
          _buffer.buffer[_state.name].push(_state);
        }
      });
    }
  }
  this.states = new this.StateBuffer(),

  // actions
  this.Action = function () {

  }
}

var ui = new UI();
