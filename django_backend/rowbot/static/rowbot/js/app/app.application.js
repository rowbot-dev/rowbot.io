
var App = (App || {});
App.application = function () {
  return ui._component('app', {
    style: {
      'height': '100%',
      'width': '100%',
      'top': '0%',
      'top': '0%',
      '.hidden': {
        'display': 'none',
      },
      '.notouch': {
        'pointer-events': 'none',
      },
    },
    children: [
      ui._component('sidebar', {
        style: {
          'height': '100%',
          'width': '200px',
          'border-right': '1px solid black',
          'float': 'left',
        },
        children: [
          ui._component('crest', {
            style: {
              'height': '250px',
              'width': '100%',
            },
          }),
          Components.buttonGroup('menu', {
            style: {
              '.button': {
                'min-height': '50px',
                'height': 'auto',
                'width': '100%',
                'border-bottom': '1px solid black',
              },
              '.first': {
                'border-top': '1px solid black',
              },
              '.hover': {
                'border-color': 'red',
              },
              '.before': {
                'border-bottom-color': 'red',
              },
              '.sub': {
                'width': '100%',
              },
              '.sub .button': {
                'position': 'relative',
                'width': '80%',
                'left': '20%',
              },
            },
            children: [
              Components.button('events', {
                html: 'Events',
              }),
              Components.button('members', {
                html: 'Members',
              }),
              Components.button('roles', {
                html: 'Roles',
              }),
              Components.button('account', {
                html: 'Account',
              }),
            ],
          }),
        ],
      }),
      ui._component('interfaces', {
        style: {
          'height': '100%',
          'width': 'calc(100% - 200px)',
          'float': 'left',
          '.interface': {
            'position': 'absolute',
            'height': '100%',
            'width': '100%',
            'top': '0%',
            'top': '0%',
          },
        },
        children: [
          // App.interfaces.main(),
          // App.interfaces.club(),
          // App.interfaces.event(),
          // App.interfaces.team(),
          // App.interfaces.asset(),
          // App.interfaces.account(),
          // App.interfaces.role.main(),
          App.interfaces.member(),
        ],
      }),
    ],
  }).then(function (_app) {

    var _buttons = _app.get('sidebar.menu');
    var _roles = _buttons.get('roles');

    // modify buttons
    _buttons.children().forEach(function (_button) {
      // add expanding animation and child style
      // 1. expand
      // 2. children
      let _sub = _button.get('sub');
      if (_sub) {
        _sub.children().forEach(function (_child) {

        });
      }
    });

    _roles.click = function (event) {
      return ui.states.call('roles');
    }

    return _app;
  });
}
