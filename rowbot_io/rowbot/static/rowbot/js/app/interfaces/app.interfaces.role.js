
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.role = function () {
  return ui._component('role', {
    classes: ['interface'],

  }).then(function (_role) {
    return _role;
  });
}
