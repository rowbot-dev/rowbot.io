
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.role = (App.interfaces.role || {});
App.interfaces.role.root = (App.interfaces.role.root || {});
App.interfaces.role.root.focus = function () {
  return Components.panel('focus', {
    classes: ['panel'],
    style: {
      'width': '385px',
    },
    children: [
      // member and member list
      Components.field('member'),
      Components.list('members'),

      // role and role list
      Components.field('role'),
      Components.list('models'),

      // Upcoming events
      Components.list('events'),

      // Event history
      Components.button('previous'),
    ],
  }).then(function (_focus) {
    return _focus;
  });
}
