var Auth = (Auth || {});
Auth.interfaces = (Auth.interfaces || {});
Auth.interfaces.login = function () {
  return ui._component('login', {
    classes: ['interface'],
    children: [
      ui._component('container', {
        classes: ['centred'],
        style: {
          'height': '400px',
          'width': '400px',
        },
        children: [
          Components.text('text', {
            title: 'Login',
            value: 'Please log in here'
          }),
          Components.form('form', {
            children: [
              Components.input('username', {
                style: {
                  'border': '1px solid black',
                },
              }),
              Components.input('password', {
                style: {
                  'border': '1px solid black',
                },
                properties: {
                  'type': 'password',
                },
              }),
              Components.button('submit', {
                style: {
                  'height': '40px',
                  'width': '100px',
                  'border': '1px solid black',
                },
                html: 'Login',
              }),
            ],
          }),
        ],
      }),
    ],
  }).then(function (_login) {

    // send form to login
    var _form = _login.get('container.form');
    _form.send = function (results) {
      var data = {};
      results.forEach(function (result) {
        data[result.name] = result.value;
      });
      return api.request('/auth/', 'POST', data).then(function (result) {
        if (result.success) {
          window.location = '/';
        } else {
          return _form.error();
        }
      });
    }

    return _login;
  });
}
