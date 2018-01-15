
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.member = (App.interfaces.member || {});
App.interfaces.member.new = function () {
  return ui._component('new', {
    classes: ['panel', 'hidden'],
    children: [

      // title
      Components.text('title', {
        title: 'Create a new user',
      }),

      // form
      Components.form('form', {
        children: [
          // member first name
          Components.input('first', {
            placeholder: 'First name...',
          }),

          // member last name
          Components.input('last', {
            placeholder: 'Last name...',
          }),

          // member email
          Components.input('email', {
            placeholder: 'Email...',
            type: 'email',
          }),

          // member role models
          Components.text('modeltitle', {
            title: 'Available roles',
          }),
          Components.list('models', {
            style: {
              'height': '40px',
            },
          }),

          // submit button
          Components.button('submit', {
            style: {
              'height': '40px',
              'width': '100px',
              'border': '1px solid black',
              'float': 'left',
            },
            html: 'Create',
          }),

          // information
          Components.button('info', {
            classes: ['hidden'],
            style: {
              'height': '40px',
              'border': '1px solid black',
              'margin-left': '10px',
              'padding': '10px',
              'float': 'left',
              '.error': {
                'border': '1px solid red',
                'color': 'red',
              },
              '.success': {
                'border': '1px solid green',
                'color': 'green',
              },
            },
            html: 'Loading...',
          }),
        ],
      }),
    ],
  }).then(function (_new) {
    return _new;
  });
}
