
/*

The role interface should show a list of roles and any individual role.

What roles to display:
1. Admin: all users' roles
2. User: only their roles

*/

var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.role = function () {
  return ui._component('role', {
    classes: ['interface'],
    children: [
      Components.list('list', {

      }),
      ui._component('single', {
        classes: ['interface'],
      }),
    ],
  }).then(function (_role) {

    var _list = _role.get('list');

    return _role;
  });
}
