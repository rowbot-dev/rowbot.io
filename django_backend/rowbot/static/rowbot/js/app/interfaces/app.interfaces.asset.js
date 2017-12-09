
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.asset = function () {
  return ui._component('asset', {
    classes: ['interface'],

  }).then(function (_asset) {
    return _asset;
  });
}
