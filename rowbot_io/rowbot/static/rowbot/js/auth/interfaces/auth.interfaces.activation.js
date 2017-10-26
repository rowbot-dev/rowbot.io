var Auth = (Auth || {});
Auth.interfaces = (Auth.interfaces || {});
Auth.interfaces.activation = function () {
  return ui._component('activation', {

  }).then(function (_activation) {
    return _activation;
  });
}
