
var App = (App || {});
App.application = function () {
  return ui._component('app', {
    style: {
      'height': '100%',
      'width': '100%',
      'top': '0%',
      'top': '0%',
      '.interface': {
        'position': 'absolute',
        'height': '100%',
        'width': '100%',
        'top': '0%',
        'top': '0%',
      },
    },
    children: [
      App.interfaces.main(),
      // App.interfaces.club(),
      // App.interfaces.event(),
      // App.interfaces.team(),
      // App.interfaces.role(),
      // App.interfaces.asset(),
    ],
  });
}
