var App = (App || {});
App.components = (App.components || {});
App.components.field = function (name, args) {
  args = (args || {});
  return ui._component((args.name || 'field'), {

  }).then(function (_field) {
    return _field;
  });
}
