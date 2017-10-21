var UI = function () {

  // component object
  this.Component = function (name) {
    this.name = name;
    this._ = {
      children: {
        buffer: [],
        rendered: [],
      },
      after: undefined,
      root: undefined,
      is: {
        rendered: false,
      },
    };
  }
  this.Component.prototype = {
    update: function (args) {
      let _this = this;
      _.l('update', _this.name);
      _this._.after = args.after;
      _this._.root = args.root;
      return _.all([
        _this.style(args.style),
        _this.properties(args.properties),
        _this.addChildren(args.children),
      ]).then(function () {
        return _this;
      });
    },

    // pre-render
    style: function (style) {

    },
    properties: function (properties) {

    },
    addChildren: function (children) {
      let _this = this;
      children = (children || []);
      return _.ordered(children.map(function (unresolved) {
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
      // root, after, indices
      return child.render();
    },
    bufferChild: function (child) {
      var _this = this;
      return _.p(function () {
        child._.parent = _this;
        _this._.children.buffer.push(child);
      });
    },

    // post-render
    classes: {
      add: function (classes) {

      },
      remove: function (classes) {

      },
    },

    // element
    element: function () {

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
      return _this.setID().then(function (_id) {
        _.l('render', _id);
        _this._.is.rendered = true;
        return _this.addChildren(_this._.children.buffer);
      });
    },
  }
  this._component = function (name, args) {
    let _component = new this.Component(name);
    return _component.update(args);
  }


  // state object
  this.State = function (name) {

  }
  this.State.prototype = {

  }
  this._state = function () {

  }
  this.state = function () {

  }

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
var C = function () {
  return ui._component(arguments);
}
