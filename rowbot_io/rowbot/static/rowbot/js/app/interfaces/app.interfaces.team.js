
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.team = function () {
  return ui._component('team', {
    classes: ['interface'],

  }).then(function (_team) {
    return _team;
  });
}
