
var Test = (Test || {});
Test.components = (Test.components || {});
Test.components.input = function (name, args) {
  return ui._component(name, _.merge({
    style: {
      'position': 'relative',
      'height': '40px',
      'width': '200px',
    },
    children: [
      ui._component('input', {
        tag: 'input',
        properties: {
          type: 'text',
        },
        style: {
          'position': 'absolute',
          'height': '100%',
          'width': '100%',
          'box-sizing': 'border-box',
          'padding-left': '8px',
          'font-size': '15px',
          'background-color': 'transparent',
          '-webkit-box-shadow': 'inset 0 0px 0px rgba(0, 0, 0, .075), 0 0 0px rgba(102, 175, 233, .6)',
          'box-shadow': 'inset 0 0px 0px rgba(0, 0, 0, .075), 0 0 0px rgba(102, 175, 233, .6),',
          'outline': 'none',
          'border': '0px',
        },
      }),
      ui._component('suggestion', {

      }),
      ui._component('message', {

      }),
    ],
  }, args)).then(function (_input) {

    // set and get content
    // set and get position, blur, and focus
    // set and remove message and errors
    _input.map = function (value) {
      return value;
    }

    _input.get('input').setBindings({
      'keypress': function (_this, event) {
        var _element = _this.element();
        if (event.which && ![8, 13, 16, 17, 18, 32, 37, 38, 39, 40, 91, 93].contains(event.which)) {
          var start = _element.selectionStart, end = _element.selectionEnd;
          _element.value = _element.value.slice(0, start) + _input.map(event.key) + _element.value.slice(end);

          // Move the caret
          _element.setSelectionRange(start + 1, start + 1);

          event.preventDefault();
        }
      },
    });

    return _input;
  });
}
