var Auth = (Auth || {});
Auth.interfaces = (Auth.interfaces || {});
Auth.interfaces.signup = function () {
  return ui._component('signup', {

  }).then(function (_signup) {
    return _signup;
  });
}
