
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.main = function () {
  return ui._component('main', {
    classes: ['interface'],
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
                classes: ['first'],
              }),
              Components.button('events', {
                html: 'Events',
              }),
              Components.button('clubs', {

              }),
              Components.button('roles', {

              }),
              Components.button('teams', {

              }),
              Components.button('assets', {

              }),
            ],
          }),
        ],
      }),
      ui._component('content', {
        style: {
          'height': '100%',
          'width': 'calc(100% - 200px)',
          'float': 'left',
        },
        children: [
          ui._component('events', {
            children: [
              // Components.list('active', {
              //
              // }),
              // Components.list('available', {
              //
              // }),
            ],
          }),
        ],
      }),
    ],
  }).then(function (_main) {
    return _main;
  });
}
