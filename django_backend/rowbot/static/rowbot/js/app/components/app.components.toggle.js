var App = (App || {});
App.components = (App.components || {});
App.components.toggle = function (name, args) {
  args = (args || {});
  return ui._component((args.name || 'toggle'), {

  }).then(function (_toggle) {

    _toggle.update = function (args) {
      return _.p();
    }

    return _toggle;
  });
}
