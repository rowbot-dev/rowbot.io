
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.main = function () {
  return ui._component('main', {
    classes: ['interface'],
    children: [
      
    ],
  }).then(function (_main) {
    return _main;
  });
}
