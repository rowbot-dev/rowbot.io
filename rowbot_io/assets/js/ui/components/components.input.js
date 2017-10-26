
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
      // ui._component('suggestion', {
      //
      // }),
      ui._component('message', {

      }),
    ],
  }, args)).then(function (_input) {

    // set and get content
    // set and get position, blur, and focus
    // set and remove message and errors
    _input.input = function (value, event) {

    }

    _input.get('input').setBindings({
      'input': function (_this, event) {
        return _input.input(_this.element().value, event);
      },
    });

    return _input;
  });
}
