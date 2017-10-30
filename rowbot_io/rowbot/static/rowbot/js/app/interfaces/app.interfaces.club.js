
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.club = function () {
  return ui._component('club', {
    classes: ['interface'],

  }).then(function (_club) {
    return _club;
  });
}
