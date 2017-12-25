
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
                'height': '50px',
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
            },
            children: [
              Components.button('account', {
                html: 'Account',
              }),
              Components.button('events', {
                html: 'Events',
              }),
              Components.button('roles', {
                html: 'Roles',
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
          App.interfaces.main(),
          // App.interfaces.club(),
          // App.interfaces.event(),
          // App.interfaces.team(),
          // App.interfaces.asset(),
          App.interfaces.account(),
          App.interfaces.role(),
        ],
      }),
    ],
  }).then(function (_app) {

    var _buttons = _app.get('sidebar.menu');
    var _roles = _buttons.get('roles');

    _roles.click = function (event) {
      return ui.states.call('roles');
    }

    return _app;
  });
}
