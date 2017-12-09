
var Components = (Components || {});
Components.button = function (name, args) {
  return ui._component(name, _.merge({
    classes: ['button'],
    style: {
      'padding-top': '10px',
      'text-align': 'center',
      'cursor': 'pointer',
    },
  }, args)).then(function (_button) {

    _button.click = function (event) {
      return _.p();
    }

    _button.setBindings({
      'click': function (_this, event) {
        return _this.click();
      },
      'mouseover': function (_this, event) {
        
      },
    });

    return _button;
  });
}
