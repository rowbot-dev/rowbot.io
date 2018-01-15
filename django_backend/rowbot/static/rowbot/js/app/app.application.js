
var App = (App || {});
App.application = function () {
  return ui._component('app', {
    style: {
      'height': '100%',
      'width': '100%',
      'top': '0%',
      'top': '0%',
      ' .hidden': {
        'display': 'none',
      },
      ' .notouch': {
        'pointer-events': 'none',
      },
      ' .interface': {
        'position': 'absolute',
        'height': '100%',
        'width': '100%',
        'top': '0%',
        'top': '0%',
      },
    },
    children: [
      // components
      // App.components.sidebar(),

      // interfaces
      App.interfaces.load(),
      // App.interfaces.account(),
      App.interfaces.club.main(),
    ],
  }).then(function (_app) {
    return _app;
  });
}
