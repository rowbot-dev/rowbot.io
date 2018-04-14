
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
        'width': '100%',
        'height': '100%',
      },
      ' .panel': {
        'width': 'calc(100% - 200px)',
      }
    },
    children: [
      // interfaces
      App.interfaces.load(),
      // App.interfaces.account(),
      App.interfaces.club.main(),
      App.interfaces.event.main(),

      // components
      App.components.sidebar(),
    ],
  }).then(function (_app) {
    return _app;
  });
}
