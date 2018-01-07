
var Components = (Components || {});
Components.input = function (name, args) {
  args = (args || {});
  return ui._component(name, _.merge({
    style: {
      'position': 'relative',
      'height': '40px',
      'width': '385px',
    },
    properties: {

    },
    children: [
      ui._component('input', {
        tag: 'input',
        properties: _.merge({
          type: 'text',
          placeholder: (args.placeholder || 'Search...'),
        }, args.properties),
        style: {
          'position': 'absolute',
          'height': '100%',
          'width': 'calc(100% - 100px)',
          'top': '0px',
          'box-sizing': 'border-box',
          'padding-left': '8px',
          'font-size': '15px',
          'background-color': 'transparent',
          '-webkit-box-shadow': 'inset 0 0px 0px rgba(0, 0, 0, .075), 0 0 0px rgba(102, 175, 233, .6)',
          'box-shadow': 'inset 0 0px 0px rgba(0, 0, 0, .075), 0 0 0px rgba(102, 175, 233, .6),',
          'outline': 'none',
          'border': '1px solid black',
        },
      }),
      Components.button('search', {
        style: {
          'position': 'absolute',
          'height': '40px',
          'width': '90px',
          'right': '0px',
          'top': '0px',
          'border': '1px solid black',
        },
        html: 'Search',
      }),
      Components.button('message', {

      }),
      Components.button('clear', {

      }),
    ],
  }, args)).then(function (_input) {

    // set and get content
    // set and get position, blur, and focus

    // bound to click
    _input.submit = function (value, event) {

    }

    // bound to input event
    _input.input = function (value, event) {

    }

    // bound to keypress event
    _input.keypress = function (value, event) {

    }

    // validation
    _input.type = (args.type || 'text');
    _input.message = (args.message || 'Required');
    _input.validators = {
      date: function () {

      },
      email: function () {

      },
      text: function () {
        return _input.value !== '';
      },
    }
    _input.validate = function () {
      return _input.validators[_input.type]();
    }
    _input.export = function () {
      _input.value = _input.get('input').element().value;
      if (_input.validate()) {
        return _.p({
          name: _input.name,
          validated: true,
          value: _input.value,
        });
      } else {
        return _input.error();
      }
    },

    // errors and messages
    _input.error = function (message) {
      message = (message || _input.message);
      return _.p({
        name: _input.name,
        validated: false,
        value: message,
      });
    }

    _input.get('input').setBindings({
      'input': function (_this, event) {
        return _input.input(_this.element().value, event);
      },
      'keypress': function (_this, event) {
        return _input.keypress(_this.element().value, event);
      },
    });

    _input.get('search').setBindings({
      'click': function (_this, event) {
        return _input.submit(_this.element().value, event);
      },
    });

    return _input;
  });
}
