var App = (App || {});
App.components = (App.components || {});
App.components.new = function (name, args) {
  args = (args || {});
  return ui._component((args.name || 'new'), {

  }).then(function (_new) {
    return _new;
  });
}
