var App = (App || {});
App.components = (App.components || {});
App.components.field = function (name, args) {
  args = (args || {});
  return ui._component((name || 'field'), _.merge({
    children: [
      Components.input('content', {
        
      }),
    ],
  }, args)).then(function (_field) {

    _field.update = function (args) {
      return _.p();
    }

    return _field;
  });
}
