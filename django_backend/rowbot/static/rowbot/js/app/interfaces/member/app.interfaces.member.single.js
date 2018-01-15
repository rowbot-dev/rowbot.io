
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.member = (App.interfaces.member || {});
App.interfaces.member.single = function () {
  return ui._component('single', {
    classes: ['panel', 'hidden'],
    children: [
      // member name
      Components.text('name'),

      // member email
      Components.text('email', {
        style: {
          'display': 'inline-block',
        },
      }),

      // member activation
      Components.text('activation', {
        style: {
          '.activated': {
            'color': `${Color.green.dark}`,
            'border': `1px solid ${Color.green.dark}`,
          },
          'color': 'red',
          'border': '1px solid red',
          'display': 'inline-block',
          'padding-left': '5px',
          'padding-right': '5px',
          'margin-left': '8px',
          'height': '24px',
          ' p': {
            'margin-top': '4px',
          },
        },
      }),

      // member role list
      Components.list('roles', {

      }),
    ],
  }).then(function (_single) {
    return _single;
  })
}
