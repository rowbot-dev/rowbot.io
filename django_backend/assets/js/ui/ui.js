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
              return $(element).css(_this._.style[''], {queue: false}).promise();
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
          _this.element().innerHTML = _this._.html;
        }
      });
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
        _this._.children.buffer.push(child);
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
          return _.p(function () {
            element.classList.remove(_class);
          });
        }
      }
    },
    removeProperty: function (properties) {

    },
    removeBinding: function (key) {
      var _this = this;
      var _binding = _this._.bindings[key];
      delete _this._.bindings[key];

      if (_this._.is.rendered) {
        var element = _this.element();
        return _.p(function () {
          element.removeEventListener(key, _binding);
        });
      }
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
          _this.setHTML(),
        ]).then(function () {
          // 3. go down through children
          return _this.setChildren();
        });
      }).then(function () {
        return _this;
      });
    },
    hide: function (duration) {
      var _this = this;
      return _this.setStyle({'opacity': '0.0'}).then(function () {
        return _this.setClasses('hidden');
      });
    },
    show: function (duration) {
      var _this = this;
      return _this.removeClass('hidden').then(function () {
        return _this.setStyle({'opacity': '1.0'});
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
        return sub['_'] || [];
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
}

var ui = new UI();
