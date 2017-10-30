
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.event = function () {
  return ui._component('event', {
    classes: ['interface'],

  }).then(function (_event) {
    return _event;
  });
}
