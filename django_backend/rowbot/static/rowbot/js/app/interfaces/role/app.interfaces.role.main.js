
/*

The role interface should show a list of roles and any individual role.

What roles to display:
1. Admin: all users' roles
2. User: only their roles

*/

var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.role = (App.interfaces.role || {});
App.interfaces.role.main = function () {
  return ui._component('role', {
    classes: ['interface'],
    children: [
      // App.interfaces.role.model.main(),
      App.interfaces.role.root.main(),
    ],
  });
}
