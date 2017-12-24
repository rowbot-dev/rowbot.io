
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.account = function () {
  return ui._component('account', {
    classes: ['interface'],
    children: [
      // member name
      // member email
      // change email
      // change password
    ],
  }).then(function (_account) {
    return _account;
  });
}
